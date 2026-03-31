# Architecture — Topic Modelling using Python

## System Overview

This project implements topic modelling using Latent Dirichlet Allocation (LDA) to discover hidden thematic structures in a collection of text documents. The pipeline takes raw articles as input and produces topic assignments for each document.

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          TOPIC MODELLING PIPELINE                       │
└─────────────────────────────────────────────────────────────────────────┘

  INPUT                    PROCESSING                   OUTPUT
  ─────                    ─────────                    ──────

┌──────────────┐     ┌──────────────────┐      ┌──────────────────────────┐
│  articles    │     │                  │      │   topic_results.csv     │
│    .csv       │────>│  Data Loader    │      │   - title               │
│               │     │                  │      │   - text                │
│  Columns:     │     │  - Read CSV     │      │   - cleaned_text        │
│  - title      │     │  - Validate     │      │   - topic               │
│  - text       │     │    columns      │      │   - topic_label         │
└──────────────┘     └────────┬─────────┘      └──────────────────────────┘
                               │
                               v
                        ┌──────────────────┐
                        │  Text Preprocessor│
                        │                  │
                        │  - Lowercase     │
                        │  - Remove        │
                        │    punctuation   │
                        │  - Remove        │
                        │    stopwords     │
                        └────────┬─────────┘
                                 │
                                 v
                        ┌──────────────────┐
                        │ CountVectorizer  │
                        │                  │
                        │  - Bag-of-words  │
                        │  - Document-    │
                        │    Term Matrix  │
                        └────────┬─────────┘
                                 │
                                 v
                        ┌──────────────────┐
                        │    LDA Model     │
                        │                  │
                        │  - k = 5 topics  │
                        │  - 50 iterations│
                        │  - Online learning│
                        └────────┬─────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    v                         v
            ┌──────────────┐          ┌──────────────┐
            │ Topic Terms │          │ Doc Topics   │
            │  (top words)│          │ (assignment) │
            └──────────────┘          └──────────────┘
```

## Data Flow

1. **Input**: articles.csv loaded with pandas
2. **Preprocess**: Text cleaned (lowercase, punctuation removal, stopword filtering)
3. **Vectorize**: CountVectorizer creates document-term matrix
4. **Model**: LDA discovers 5 latent topics
5. **Assign**: Each document gets assigned to dominant topic
6. **Output**: Results saved to topic_results.csv

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Python over R | Matches project folder name, broader ML ecosystem |
| CountVectorizer | Simple, effective for topic discovery |
| k=5 topics | Suitable for small dataset (5 articles) |
| Online LDA | Memory efficient, faster for small datasets |
| CSV I/O | Simple, no database needed for this scale |

## External Dependencies

| Dependency | Source | Purpose |
|------------|--------|---------|
| pandas | PyPI | Data I/O |
| numpy | PyPI | Numerical operations |
| scikit-learn | PyPI | LDA, CountVectorizer |

## Output Artifacts

| File | Description |
|------|-------------|
| topic_results.csv | Input articles with topic assignments |
| articles.csv | Original input data |

---

**Last Updated**: 2026-03-23