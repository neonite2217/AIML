# Lab Project: Text Summarization Model using LLMs

# 1. Choose T5 model size
# Models: t5-small, t5-base, t5-large
MODEL_NAME = "t5-small"

# 2. Install transformers
# pip install transformers sentencepiece

from transformers import T5Tokenizer, T5ForConditionalGeneration

# 3. Load tokenizer + model
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

# Some text to summarize
text = """
The James Webb Space Telescope (JWST) is a space telescope designed primarily to conduct infrared astronomy.
As the largest optical telescope in space, its high resolution and sensitivity allow it to view objects too old,
distant, or faint for the Hubble Space Telescope. This enables investigations across many fields of astronomy
and cosmology, such as observation of the first stars and the formation of the first galaxies, and detailed
atmospheric characterization of potentially habitable exoplanets.
"""

# 4. Prefix input with "summarize: "
prefixed_text = "summarize: " + text

# 5. Tokenize with truncation/max length
input_ids = tokenizer.encode(prefixed_text, return_tensors="pt", max_length=512, truncation=True)

# 6. Generate summary using beam search/length penalty
summary_ids = model.generate(input_ids,
                               num_beams=4,
                               length_penalty=2.0,
                               max_length=150,
                               min_length=40,
                               no_repeat_ngram_size=2)

# 7. Decode and evaluate quality
summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

print("Original Text:")
print(text)
print("\nGenerated Summary:")
print(summary)
