# Architecture — Text Classification Pipeline

## System Overview

This text classification pipeline is a classical machine learning system that processes raw text documents, converts them into numerical features, trains a Naive Bayes classifier, and evaluates its performance. The system is implemented as a standalone R script that can be executed from the command line.

The pipeline demonstrates fundamental NLP concepts including text preprocessing, feature extraction using bag-of-words representation, and probabilistic classification using the Naive Bayes algorithm.

---

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Text Classification Pipeline                  │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Data Layer │────▶│ Preprocessing│────▶│Feature Layer │
└──────────────┘     └──────────────┘     └──────────────┘
       │                     │                     │
       ▼                     ▼                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│newsgroups.csv│     │  quanteda    │     │     DFM      │
│(text, topic) │     │  corpus/     │     │(doc x term  │
│              │     │  tokens/     │     │   matrix)    │
└──────────────┘     │  dfm         │     └──────────────┘
                     └──────────────┘            │
                                                  │
                                                  ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Evaluation  │◀────│  Prediction  │◀────│  Model Layer │
└──────────────┘     └──────────────┘     └──────────────┘
       │                     │                     │
       ▼                     ▼                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Confusion  │     │   Predicted  │     │   Naive      │
│    Matrix    │     │    Labels    │     │   Bayes      │
│   Accuracy   │     │              │     │  (e1071)     │
└──────────────┘     └──────────────┘     └──────────────┘
```

---

## Data Flow

### Step 1: Data Ingestion

```
Input: newsgroups.csv
       ├── text: "The new graphics card is amazing for gaming."
       └── topic: "comp.graphics"

Process:
1. Check if file exists
2. If not, generate sample data
3. Load into R data frame using read_csv()
4. Validate minimum row count (≥2)
```

### Step 2: Text Preprocessing

```
Input: Raw text documents

Process:
1. Create corpus from data frame
   corpus ← corpus(news, text_field = "text")

2. Tokenize with cleaning
   tokens ← tokens(corpus, 
                   remove_punct = TRUE,
                   remove_numbers = TRUE,
                   remove_symbols = TRUE)

3. Remove stopwords
   tokens ← tokens_remove(tokens, stopwords("english"))

Output: Clean tokenized documents
```

### Step 3: Feature Extraction

```
Input: Clean tokens

Process:
1. Build Document-Feature Matrix
   dfm ← dfm(tokens)

Output: DFM (sparse matrix)
        Rows: Documents
        Columns: Terms (features)
        Values: Term frequency counts
```

### Step 4: Train/Test Split

```
Input: DFM with n documents

Process:
1. Set random seed for reproducibility
2. Sample 80% for training
3. Remaining 20% for testing
4. Extract corresponding labels

Output:
   train_dfm (80% of documents)
   test_dfm (20% of documents)
   train_labels
   test_labels
```

### Step 5: Model Training

```
Input: train_dfm, train_labels

Process:
1. Train Naive Bayes classifier
   model ← textmodel_nb(train_dfm, train_labels)

Algorithm:
   - Multinomial Naive Bayes
   - P(class|document) ∝ P(class) × ∏ P(word|class)^count

Output: Trained nb_model
```

### Step 6: Prediction

```
Input: nb_model, test_dfm

Process:
1. Predict class probabilities
2. Select class with highest probability

Output: predicted_classes (vector of labels)
```

### Step 7: Evaluation

```
Input: predicted_classes, test_labels

Process:
1. Build confusion matrix
   conf_matrix ← table(predicted, actual)

2. Calculate accuracy
   accuracy ← sum(diagonal) / sum(all)

Output:
   - Confusion matrix table
   - Accuracy score (0.0 to 1.0)
```

---

## Key Design Decisions

### 1. Why R?

**Decision**: Use R as the implementation language

**Rationale**:
- Excellent statistical computing ecosystem
- Native support for text analysis via quanteda
- Built-in data manipulation with tidyverse
- Widely used in academia and research
- Simple deployment (single script)

**Alternatives Considered**:
- Python (scikit-learn) - More popular for production ML
- Julia - Better performance but smaller ecosystem

### 2. Why Naive Bayes?

**Decision**: Use Multinomial Naive Bayes as the classifier

**Rationale**:
- Simple and interpretable
- Works well with high-dimensional text data
- Fast training and prediction
- Good baseline for text classification
- Handles sparse features well

**Alternatives Considered**:
- SVM - Better accuracy but slower
- Random Forest - More robust but less interpretable
- Deep Learning - Overkill for this dataset size

### 3. Why Bag-of-Words?

**Decision**: Use term frequency counts (bag-of-words) as features

**Rationale**:
- Simple and effective for small datasets
- No pre-trained models required
- Fast to compute
- Easy to interpret

**Alternatives Considered**:
- TF-IDF - Better for larger corpora
- Word embeddings - Require pre-trained models
- N-grams - Could improve accuracy but increase dimensionality

### 4. Why 80/20 Split?

**Decision**: Use 80% training, 20% testing split

**Rationale**:
- Industry standard for small to medium datasets
- Balances training data size vs. reliable evaluation
- With 5 samples, gives 4 train / 1 test (minimum viable)

**Alternatives Considered**:
- 70/30 split - More conservative
- Cross-validation - Better for small datasets but more complex

### 5. Why quanteda?

**Decision**: Use quanteda for text processing

**Rationale**:
- Leading R package for quantitative text analysis
- Comprehensive text preprocessing capabilities
- Efficient DFM implementation
- Well-documented and maintained

**Alternatives Considered**:
- tm package - Older, less feature-rich
- tidytext - Better for tidy data but less efficient for DFM

---

## External Dependencies

| Dependency | Purpose | Version |
|------------|---------|---------|
| R | Runtime environment | ≥4.0 |
| tidyverse | Data loading and manipulation | Latest |
| quanteda | Text processing and DFM | Latest |
| e1071 | Naive Bayes implementation | Latest |

---

## Performance Characteristics

| Metric | Expected Value |
|--------|----------------|
| Startup Time | <1 second |
| Data Loading | <1 second |
| Preprocessing | 1-2 seconds |
| Training | <1 second |
| Prediction | <1 second |
| Total Runtime | 2-5 seconds |
| Memory Usage | <100MB |

**Scalability Notes**:
- Current implementation suitable for datasets up to ~10,000 documents
- For larger datasets, consider:
  - Sampling for initial development
  - Incremental learning algorithms
  - Distributed processing (Spark, Dask)

---

## Security Considerations

1. **Input Validation**: Script validates minimum data requirements
2. **No External Calls**: No network requests or API calls
3. **No Secrets**: No API keys or credentials required
4. **File Permissions**: Standard file system permissions apply

---

## Error Handling

| Error Condition | Handling Strategy |
|-----------------|-------------------|
| File not found | Auto-generate sample data |
| Insufficient data | Error message and graceful exit |
| Package not installed | Error at library loading |
| Empty test set | Warning message, skip evaluation |
| Single document | Warning message, skip split |

---

**Document Version**: 1.0.0  
**Last Updated**: 2026-03-17  
**Author**: Ansh
