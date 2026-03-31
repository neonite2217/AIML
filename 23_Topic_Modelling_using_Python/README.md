# Topic Modelling using Python

> Discover hidden topics in documents using Latent Dirichlet Allocation (LDA)

## Tech Stack

| Component | Technology |
|-----------|-------------|
| Language | Python 3.8+ |
| ML Library | scikit-learn |
| Data Processing | pandas, numpy |
| Algorithm | Latent Dirichlet Allocation (LDA) |

## Prerequisites

- Python 3.8 or higher
- pip package manager

Required packages:
```
pandas
numpy
scikit-learn
```

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd 23_Topic_Modelling_using_Python
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install pandas numpy scikit-learn
   ```

   Or install all dependencies at once:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Topic Modelling Pipeline

Execute the main script:
```bash
python topic_modelling.py
```

### Expected Output

The script will:
1. Load articles from `articles.csv`
2. Preprocess text (lowercase, remove punctuation, stopwords)
3. Create document-term matrix
4. Fit LDA model with 5 topics
5. Assign topics to documents
6. Save results to `topic_results.csv`

### Output Files

| File | Description |
|------|-------------|
| `topic_results.csv` | Articles with assigned topics |
| `articles.csv` | Input dataset (5 sample articles) |

## Project Structure

```
23_Topic_Modelling_using_Python/
├── README.md                  # This file
├── RULES.md                   # Agent operating rules
├── AGENT_RUN_LOG.md           # Agent execution log
├── guide.txt                  # Original project specification
├── articles.csv               # Input data (5 articles)
├── topic_modelling.R          # R implementation (original)
├── topic_modelling.py         # Python implementation
└── topic_results.csv          # Generated output
```

## Architecture Overview

### Data Flow

```
articles.csv → Text Preprocessing → Document-Term Matrix → LDA Model → Topic Assignment → topic_results.csv
```

### Components

1. **Data Loader**: Reads CSV with title and text columns
2. **Text Preprocessor**: Cleans text (lowercase, remove special chars, stopwords)
3. **Vectorizer**: Creates bag-of-words document-term matrix
4. **LDA Model**: Fits topic model with k=5 topics
5. **Topic Assigner**: Assigns dominant topic to each document

## Environment Variables

No environment variables required for this project.

## Running Tests

No formal test suite exists for this project. To verify functionality:

```bash
python topic_modelling.py
```

Verify `topic_results.csv` was created with topic assignments.

## SDLC Status

See [docs/sdlc.md](docs/sdlc.md) for complete SDLC documentation.

## Common Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'sklearn'"

**Solution**: Install scikit-learn
```bash
pip install scikit-learn
```

### Issue: "FileNotFoundError: articles.csv not found"

**Solution**: Ensure you're running from the project directory:
```bash
cd 23_Topic_Modelling_using_Python
python topic_modelling.py
```

### Issue: Empty topic results or poor topic quality

**Solution**: 
- Ensure input articles.csv has sufficient text data
- Try adjusting `n_topics` parameter in the code (default: 5)
- Increase `max_iter` in LDA for more iterations

### Issue: "KeyError: 'text'" or "KeyError: 'title'"

**Solution**: Verify articles.csv has columns: `title` and `text`

### Issue: Unicode encoding errors

**Solution**: Ensure CSV file is saved with UTF-8 encoding, or add encoding parameter:
```python
pd.read_csv('articles.csv', encoding='utf-8')
```

## Contributing

This is a lab project for educational purposes. Feel free to enhance:
- Add more preprocessing options (lemmatization, n-grams)
- Implement coherence score calculation for topic selection
- Add visualization (pyLDAvis)
- Compare with NMF or BERTopic

## License

Educational project - University of Gemini