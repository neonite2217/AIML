# Lab Project: Fine-tuning LLMs on Your Own Data using PEFT/LoRA
# Robust version with offline-safe fallbacks for dataset/model loading.

import os
import random
import numpy as np
import torch

from datasets import Dataset, DatasetDict, load_dataset
from peft import LoraConfig, TaskType, get_peft_model
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    DistilBertConfig,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments,
)

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
MODEL_NAME = "distilbert-base-uncased"
DATASET_NAME = "imdb"
OUTPUT_DIR = "./lora-imdb-model"
RESULTS_DIR = "./results"
LOGS_DIR = "./logs"
CACHE_ROOT = os.path.abspath("./.cache/huggingface")

TRAIN_SIZE = 200
TEST_SIZE = 50
EPOCHS = 1
SEED = 42


# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------
def setup_environment():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(CACHE_ROOT, exist_ok=True)

    # Keep all HF writes inside project workspace.
    os.environ.setdefault("HF_HOME", CACHE_ROOT)
    os.environ.setdefault("HF_DATASETS_CACHE", os.path.join(CACHE_ROOT, "datasets"))
    os.environ.setdefault("HUGGINGFACE_HUB_CACHE", os.path.join(CACHE_ROOT, "hub"))
    os.environ.setdefault("TRANSFORMERS_CACHE", os.path.join(CACHE_ROOT, "transformers"))

    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)


def build_local_fallback_dataset(train_size: int, test_size: int) -> DatasetDict:
    positive_templates = [
        "I loved this movie. Great acting and story.",
        "Excellent film with strong performances.",
        "Amazing direction and very engaging plot.",
        "A wonderful experience. Highly recommended.",
        "Great pacing and memorable characters.",
    ]
    negative_templates = [
        "I hated this movie. It was boring and messy.",
        "Terrible film with weak acting.",
        "Poor script and confusing scenes.",
        "Waste of time. Not recommended.",
        "Disappointing story and bad execution.",
    ]

    def make_split(size: int):
        texts = []
        labels = []
        for i in range(size):
            if i % 2 == 0:
                texts.append(random.choice(positive_templates))
                labels.append(1)
            else:
                texts.append(random.choice(negative_templates))
                labels.append(0)
        return Dataset.from_dict({"text": texts, "label": labels})

    return DatasetDict({
        "train": make_split(train_size),
        "test": make_split(test_size),
    })


def load_dataset_with_fallback(train_size: int, test_size: int) -> DatasetDict:
    try:
        print("\n[1/6] Loading IMDb dataset...")
        dataset = load_dataset(DATASET_NAME)
        train_dataset = dataset["train"].shuffle(seed=SEED).select(range(train_size))
        test_dataset = dataset["test"].shuffle(seed=SEED).select(range(test_size))
        print("  Source: IMDb (Hugging Face)")
        return DatasetDict({"train": train_dataset, "test": test_dataset})
    except Exception as exc:
        print(f"  IMDb load failed: {exc}")
        print("  Falling back to local synthetic sentiment dataset.")
        return build_local_fallback_dataset(train_size, test_size)


def load_tokenizer() -> AutoTokenizer:
    print("\n[2/6] Loading tokenizer...")
    return AutoTokenizer.from_pretrained(MODEL_NAME, local_files_only=True)


def load_model_with_fallback():
    print("\n[3/6] Loading pretrained model...")
    id2label = {0: "NEGATIVE", 1: "POSITIVE"}
    label2id = {"NEGATIVE": 0, "POSITIVE": 1}

    try:
        model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_NAME,
            num_labels=2,
            id2label=id2label,
            label2id=label2id,
            local_files_only=True,
        )
        print("  Source: local pretrained checkpoint")
        return model
    except Exception as exc:
        print(f"  Local pretrained weights unavailable: {exc}")
        print("  Falling back to randomly initialized DistilBERT config.")
        config = DistilBertConfig(num_labels=2, id2label=id2label, label2id=label2id)
        return DistilBertForSequenceClassification(config)


def tokenize_dataset(dataset: DatasetDict, tokenizer: AutoTokenizer) -> DatasetDict:
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            padding=False,
            truncation=True,
            max_length=256,
        )

    print("  Tokenizing training data...")
    tokenized_train = dataset["train"].map(tokenize_function, batched=True, remove_columns=["text"])
    print("  Tokenizing test data...")
    tokenized_test = dataset["test"].map(tokenize_function, batched=True, remove_columns=["text"])

    tokenized_train = tokenized_train.rename_column("label", "labels")
    tokenized_test = tokenized_test.rename_column("label", "labels")

    tokenized_train.set_format("torch")
    tokenized_test.set_format("torch")

    return DatasetDict({"train": tokenized_train, "test": tokenized_test})


def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)

    accuracy = accuracy_score(labels, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels,
        predictions,
        average="binary",
        zero_division=0,
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def main():
    setup_environment()

    print("=" * 60)
    print("Fine-tuning LLMs with PEFT/LoRA")
    print("=" * 60)
    print(f"Model: {MODEL_NAME}")
    print(f"Dataset: {DATASET_NAME}")
    print(f"Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    print(f"Train samples: {TRAIN_SIZE} | Test samples: {TEST_SIZE} | Epochs: {EPOCHS}")
    print("=" * 60)

    dataset = load_dataset_with_fallback(TRAIN_SIZE, TEST_SIZE)
    print(f"  Training samples: {len(dataset['train'])}")
    print(f"  Test samples: {len(dataset['test'])}")

    tokenizer = load_tokenizer()
    tokenized = tokenize_dataset(dataset, tokenizer)

    model = load_model_with_fallback()

    print("\n[4/6] Configuring LoRA (PEFT)...")
    lora_config = LoraConfig(
        task_type=TaskType.SEQ_CLS,
        r=8,
        lora_alpha=16,
        lora_dropout=0.1,
        bias="none",
        target_modules=["q_lin", "v_lin"],
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    print("\n[5/6] Configuring training...")
    training_args = TrainingArguments(
        output_dir=RESULTS_DIR,
        learning_rate=2e-4,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        num_train_epochs=EPOCHS,
        weight_decay=0.01,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        logging_dir=LOGS_DIR,
        logging_steps=25,
        report_to="none",
        fp16=torch.cuda.is_available(),
        seed=SEED,
    )

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["test"],
        processing_class=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )

    print("\n[6/6] Starting training...")
    print("=" * 60)
    trainer.train()

    print("\n" + "=" * 60)
    print("Evaluating model...")
    print("=" * 60)
    eval_results = trainer.evaluate()

    print("\nEvaluation Results:")
    for key, value in eval_results.items():
        if isinstance(value, (int, float)):
            print(f"  {key}: {value:.4f}")

    print("\n" + "=" * 60)
    print("Saving model...")
    print("=" * 60)
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"Model saved to: {OUTPUT_DIR}")

    print("\n" + "=" * 60)
    print("Testing inference on sample reviews...")
    print("=" * 60)

    test_reviews = [
        "This movie was absolutely fantastic! The acting was superb.",
        "Terrible waste of time. The plot made no sense at all.",
        "An average film, nothing special but not bad either.",
    ]

    model.eval()
    for review in test_reviews:
        inputs = tokenizer(review, return_tensors="pt", truncation=True, padding=True, max_length=256)
        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model(**inputs)
            prediction = torch.argmax(outputs.logits, dim=-1).item()
            confidence = torch.softmax(outputs.logits, dim=-1).max().item()

        sentiment = "POSITIVE" if prediction == 1 else "NEGATIVE"
        print(f"\nReview: {review}")
        print(f"Prediction: {sentiment} (confidence: {confidence:.2%})")

    print("\n" + "=" * 60)
    print("All tasks completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
