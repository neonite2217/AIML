# Tech Stack — Text Classification Pipeline

## Overview

This document details the technology stack used in the Text Classification Pipeline project, including the rationale for each choice and alternatives considered.

---

## Core Technologies

### 1. R Programming Language

**Version Required**: ≥4.0

**Purpose**: Primary implementation language

**Key Features Used**:
- Statistical computing capabilities
- Data frame manipulation
- Vectorized operations
- Package ecosystem (CRAN)

**Rationale**:
- Excellent for statistical and text analysis
- Mature ecosystem with specialized NLP packages
- Simple syntax for data manipulation
- Widely taught in academic settings

**Installation**:
```bash
# Ubuntu/Debian
sudo apt-get install r-base

# Fedora/RHEL
sudo dnf install R

# macOS
brew install r

# Windows
# Download from https://cran.r-project.org/bin/windows/base/
```

**Alternatives Considered**:
- **Python**: More popular for production ML, but R has better statistical foundations
- **Julia**: Better performance, but smaller package ecosystem
- **Scala**: Good for big data, but steeper learning curve

---

### 2. tidyverse

**Package**: `tidyverse`

**Purpose**: Data manipulation and visualization

**Key Components Used**:
- `readr`: CSV file reading (`read_csv()`)
- `tibble`: Modern data frames
- `dplyr`: Data manipulation (implied via tidyverse)

**Rationale**:
- Consistent API design across packages
- Modern R data handling standards
- Excellent documentation and community
- Pipe operator (`%\u003e%`) for readable code

**Installation**:
```r
install.packages("tidyverse")
```

**Key Functions**:
- `read_csv()`: Load data from CSV
- `tibble()`: Create sample data
- `write_csv()`: Save sample data

**Alternatives Considered**:
- **Base R**: Built-in but less consistent API
- **data.table**: Faster for large datasets but different syntax

---

### 3. quanteda

**Package**: `quanteda`

**Purpose**: Quantitative text analysis and natural language processing

**Key Features Used**:
- Corpus creation and management
- Tokenization with customizable options
- Stopword removal
- Document-Feature Matrix (DFM) construction

**Rationale**:
- Leading R package for text analysis
- Comprehensive preprocessing pipeline
- Efficient sparse matrix implementation
- Active development and maintenance

**Installation**:
```r
install.packages("quanteda")
```

**Key Functions**:
- `corpus()`: Create text corpus from data frame
- `tokens()`: Tokenize text with cleaning options
- `tokens_remove()`: Remove stopwords
- `dfm()`: Build document-feature matrix
- `ndoc()`: Get number of documents

**Processing Pipeline**:
```r
corpus ← corpus(data, text_field = "text")
tokens ← tokens(corpus, remove_punct = TRUE, 
                remove_numbers = TRUE, 
                remove_symbols = TRUE)
tokens ← tokens_remove(tokens, stopwords("english"))
dfm ← dfm(tokens)
```

**Alternatives Considered**:
- **tm**: Older package, less efficient
- **tidytext**: Better for tidy data workflows, less efficient for DFM
- **text2vec**: Good for word embeddings, more complex

---

### 4. e1071

**Package**: `e1071`

**Purpose**: Machine learning algorithms, specifically Naive Bayes

**Key Features Used**:
- `textmodel_nb()`: Multinomial Naive Bayes classifier
- `predict()`: Model prediction

**Rationale**:
- Well-established implementation
- Part of standard R ML ecosystem
- Simple interface
- Good documentation

**Installation**:
```r
install.packages("e1071")
```

**Key Functions**:
- `textmodel_nb(x, y)`: Train Naive Bayes model
  - `x`: Document-feature matrix
  - `y`: Class labels
- `predict(model, newdata)`: Predict classes

**Algorithm Details**:
- **Type**: Multinomial Naive Bayes
- **Assumption**: Feature independence (naive assumption)
- **Probability Model**: 
  ```
  P(class|doc) ∝ P(class) × ∏ P(word|class)^count
  ```

**Alternatives Considered**:
- **naivebayes**: Alternative implementation
- **klaR**: More comprehensive but complex
- **caret**: Unified ML interface, overkill for single algorithm

---

## Data Format

### Input Format: CSV

**File**: `newsgroups.csv`

**Schema**:
| Column | Type | Description |
|--------|------|-------------|
| text | character | Document content |
| topic | factor/character | Class label |

**Example**:
```csv
text,topic
"The new graphics card is amazing for gaming.","comp.graphics"
"NASA is launching a new mission to Mars.","sci.space"
```

**Rationale**:
- Universal format, easy to create/edit
- Human-readable
- Compatible with all tools
- No binary dependencies

**Alternatives Considered**:
- **JSON**: More structured but harder to edit manually
- **RDS**: R native format, not human-readable
- **Parquet**: Better for large datasets, overkill here

---

## Development Tools

### Recommended IDE

**RStudio** (optional but recommended)
- Download: https://posit.co/download/rstudio-desktop/
- Features: Syntax highlighting, debugging, package management

**Command Line**:
- `R`: Interactive R console
- `Rscript`: Run R scripts non-interactively

---

## Version Compatibility

| Component | Minimum Version | Tested Version |
|-----------|----------------|----------------|
| R | 4.0.0 | 4.3.x |
| tidyverse | 1.3.0 | 2.0.x |
| quanteda | 3.0 | 3.3.x |
| e1071 | 1.7 | 1.7.x |

---

## Package Dependencies

### Direct Dependencies
- tidyverse
- quanteda
- e1071

### Transitive Dependencies (automatically installed)
- Rcpp (for quanteda performance)
- Matrix (sparse matrix support)
- stringi (string processing)
- readr (CSV reading)
- And others...

---

## Performance Characteristics

| Operation | Package | Complexity | Notes |
|-----------|---------|------------|-------|
| Data Loading | readr | O(n) | n = number of rows |
| Tokenization | quanteda | O(n × avg_doc_length) | Highly optimized C++ |
| DFM Creation | quanteda | O(n × vocab_size) | Sparse matrix |
| Model Training | e1071 | O(n × vocab_size × classes) | Fast for small data |
| Prediction | e1071 | O(n × vocab_size) | Linear time |

---

## Security Notes

| Aspect | Status | Notes |
|--------|--------|-------|
| Network Calls | None | All processing local |
| External APIs | None | No API keys needed |
| File System | Read/Write | Standard permissions |
| Code Execution | User Level | No elevated privileges |

---

## Future Technology Considerations

### Potential Upgrades

1. **TF-IDF Weighting**
   - Package: `quanteda` (built-in)
   - Function: `dfm_tfidf()`
   - Benefit: Better feature weighting

2. **Cross-Validation**
   - Package: `caret` or `rsample`
   - Benefit: More robust evaluation

3. **Additional Classifiers**
   - SVM: `e1071::svm()`
   - Random Forest: `randomForest`
   - XGBoost: `xgboost`

4. **Text Embeddings**
   - Package: `text2vec` or `word2vec`
   - Benefit: Capture semantic meaning

5. **Deep Learning**
   - Package: `keras` or `torch`
   - Benefit: State-of-the-art accuracy

---

**Document Version**: 1.0.0  
**Last Updated**: 2026-03-17  
**Author**: Ansh
