# SDLC — Topic Modelling using Python

## 1. Requirements

- [x] Functional requirements listed
- [x] Non-functional requirements listed (performance, security, scalability)
- [x] User personas / target audience defined

### Functional Requirements

1. Load text data from CSV file (articles.csv with title and text columns)
2. Preprocess text: lowercase, remove punctuation, remove stopwords
3. Create document-term matrix using CountVectorizer
4. Fit Latent Dirichlet Allocation (LDA) model with configurable k topics
5. Assign dominant topic to each document
6. Save results to CSV output file

### Non-Functional Requirements

| Requirement | Description |
|-------------|-------------|
| Performance | Should process 5 sample articles in < 5 seconds |
| Portability | Works on any system with Python 3.8+ |
| Simplicity | No external API calls, runs offline |
| Extensibility | Easy to modify number of topics, vectorizer options |

### Target Audience

- Students learning NLP and topic modelling
- Data scientists exploring document clustering
- Researchers needing quick topic discovery

## 2. Design

- [x] Architecture diagram created
- [x] Tech stack finalised
- [ ] API contracts defined (N/A - CLI tool)
- [ ] Database schema documented (N/A)
- [ ] UI/UX wireframes (N/A)

### Architecture Diagram

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐     ┌────────────┐
│  articles   │ ──> │  Preprocessor│ ──> │ CountVectorizer │ ──> │   LDA     │
│    .csv     │     │ (clean text)  │     │   (DTM creation)│     │  Model    │
└─────────────┘     └──────────────┘     └─────────────────┘     └─────┬──────┘
                                                                      │
                                                                      v
                                                              ┌───────────────┐
                                                              │ topic_results │
                                                              │     .csv      │
                                                              └───────────────┘
```

### Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.8+ |
| Core ML | scikit-learn (LDA) |
| Data | pandas, numpy |
| Input/Output | CSV files |

## 3. Development

- [x] Coding standards followed
- [ ] Feature branches used (N/A - single project)
- [ ] Code reviewed before merge (N/A)

### Implementation Notes

- Python implementation created to match folder name "using Python"
- Original R implementation preserved in topic_modelling.R
- Both implementations produce equivalent outputs

## 4. Testing

- [ ] Unit tests written (>70% coverage) - N/A for educational lab project
- [ ] Integration tests written - N/A
- [x] Smoke test passes
- [x] Edge cases tested

### Smoke Test Results

```bash
$ python topic_modelling.py
============================================================
Topic Modelling - Python Implementation
============================================================

[1/6] Loading data...
Loaded 5 articles

[2/6] Preprocessing text...

[3/6] Creating document-term matrix...
  - DTM shape: (5, 44)

[4/6] Fitting LDA model (k=5 topics)...

[5/6] Extracting topics and assigning to documents...

[6/6] Saving results...
  - Results saved to topic_results.csv
```

**Status**: PASS

### Edge Cases Tested

1. ✅ Empty text field - handled with empty string replacement
2. ✅ Missing columns - raises ValueError with clear message
3. ✅ Missing file - raises FileNotFoundError
4. ✅ Small dataset (5 articles) - works correctly

## 5. Deployment

- [ ] Environment variables documented (.env.example) - N/A
- [ ] Deployment guide written - N/A (standalone script)
- [ ] Rollback plan documented - N/A
- [ ] CI/CD pipeline configured - N/A

## 6. Maintenance

- [x] Changelog kept up to date
- [x] Known issues tracked in docs/tasks.md
- [x] Agent log maintained

---

**SDLC Phase**: COMPLETE

**Last Updated**: 2026-03-23