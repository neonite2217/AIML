# Tasks — Text Classification Pipeline

Task backlog and enhancement tracking for the Text Classification Pipeline project.

---

## Must Have

- [x] Implement text classification pipeline - 2026-03-17
- [x] Create document-feature matrix using quanteda - 2026-03-17
- [x] Train Naive Bayes classifier - 2026-03-17
- [x] Evaluate model with confusion matrix - 2026-03-17
- [x] Create sample dataset (newsgroups.csv) - 2026-03-17
- [x] Handle edge cases (insufficient data) - 2026-03-17
- [x] Document SDLC process - 2026-03-22
- [x] Create comprehensive README - 2026-03-22
- [x] Document build process - 2026-03-22

---

## Should Have

- [ ] Implement TF-IDF weighting instead of raw counts
  - **Rationale**: Better feature weighting for larger datasets
  - **Implementation**: Use `dfm_tfidf()` from quanteda
  - **Priority**: Medium

- [ ] Add cross-validation support
  - **Rationale**: More robust evaluation for small datasets
  - **Implementation**: Use caret or rsample packages
  - **Priority**: Medium

- [ ] Support command-line arguments
  - **Rationale**: Allow custom dataset paths and parameters
  - **Implementation**: Use argparse or optparse package
  - **Priority**: Medium

- [ ] Add model persistence (save/load)
  - **Rationale**: Reuse trained models without retraining
  - **Implementation**: Use saveRDS() and readRDS()
  - **Priority**: Medium

---

## Could Have

- [ ] **Modern Transformer-Based Models**
  - Compare baseline Naive Bayes with BERT/DistilBERT
  - Use reticulate to interface with Python's Hugging Face
  - Significant performance boost expected
  - Priority: Low (advanced enhancement)

- [ ] **Systematic Hyperparameter Tuning**
  - Implement grid search or random search
  - Explore vectorization parameters (min/max doc frequency)
  - Tune classifier parameters (cost for SVM)
  - Priority: Low (optimization)

- [ ] **Explainable AI (XAI) for NLP**
  - Use LIME or DALEX to explain predictions
  - Identify influential words/phrases
  - Great for debugging and trust-building
  - Priority: Low (advanced feature)

- [ ] **Advanced Feature Engineering**
  - N-grams (bigrams, trigrams)
  - Word embeddings (word2vec, GloVe)
  - Handle imbalanced data with SMOTE
  - Priority: Low (enhancement)

- [ ] **Deploy as a Plumber API**
  - Create REST endpoint for text classification
  - Accept text input, return predicted class + confidence
  - Make model accessible to other applications
  - Priority: Low (deployment)

- [ ] **Additional Classifiers**
  - Support Vector Machine (SVM)
  - Random Forest
  - XGBoost
  - Comparison framework
  - Priority: Low (experimentation)

- [ ] **Docker Containerization**
  - Create Dockerfile with all dependencies
  - Ensure reproducible environment
  - Priority: Low (deployment)

---

## Won't Have (this release)

- [ ] Deep learning models (Keras, PyTorch)
  - **Reason**: Overkill for this dataset size and educational purpose
  - **Future**: Consider for production deployment

- [ ] Real-time streaming classification
  - **Reason**: Out of scope for batch processing pipeline
  - **Future**: Would require different architecture

- [ ] Distributed processing (Spark, Hadoop)
  - **Reason**: Dataset is small, doesn't need distributed computing
  - **Future**: Consider for web-scale datasets

- [ ] Web interface/UI
  - **Reason**: CLI-focused educational project
  - **Future**: Could add Shiny app

- [ ] Automated model retraining
  - **Reason**: Static dataset, not a production system
  - **Future**: For MLOps pipeline

---

## Done

- [x] Create text classification pipeline in R - 2026-03-17
- [x] Implement text preprocessing (tokenization, stopword removal) - 2026-03-17
- [x] Create DFM (Document-Feature Matrix) - 2026-03-17
- [x] Implement train/test split - 2026-03-17
- [x] Train Naive Bayes classifier - 2026-03-17
- [x] Evaluate with confusion matrix and accuracy - 2026-03-17
- [x] Create sample dataset - 2026-03-17
- [x] Write comprehensive README.md - 2026-03-22
- [x] Document SDLC in docs/sdlc.md - 2026-03-22
- [x] Document architecture in docs/architecture.md - 2026-03-17
- [x] Document tech stack in docs/tech_stack.md - 2026-03-17
- [x] Create CHANGELOG.md - 2026-03-22
- [x] Create agent_log.md - 2026-03-22
- [x] Create BUILD_LOG.md - 2026-03-22
- [x] Add troubleshooting guide to README - 2026-03-22
- [x] Update project checklist - 2026-03-22

---

## Task Statistics

| Category | Count | Status |
|----------|-------|--------|
| Must Have | 9 | 100% Complete |
| Should Have | 4 | 0% Complete |
| Could Have | 7 | 0% Complete |
| Won't Have | 5 | N/A |
| Done | 14 | 100% Complete |

---

**Last Updated**: 2026-03-22  
**Version**: 1.0.0
