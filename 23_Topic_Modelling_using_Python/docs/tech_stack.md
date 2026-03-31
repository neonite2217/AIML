# Tech Stack — Topic Modelling using Python

## Language

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Primary Language | Python 3.8+ | Project folder name specifies Python; scikit-learn is best-in-class for LDA |
| Alternative | R (topic_modelling.R) | Original implementation preserved |

## Core Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| pandas | >= 1.0 | Data loading and manipulation |
| numpy | >= 1.0 | Numerical operations |
| scikit-learn | >= 0.23 | LDA implementation, CountVectorizer |

## Why This Stack?

### Python vs R

- **scikit-learn** provides robust, well-tested LDA implementation
- **pandas** offers excellent CSV handling
- Python ecosystem more widely used in production ML pipelines

### LDA Algorithm

- **Latent Dirichlet Allocation** is the standard approach for topic modelling
- Unsupervised - no labeled data required
- Interpretable results with top words per topic

### CountVectorizer

- Bag-of-words approach sufficient for topic discovery
- Configurable stopwords, max features, n-gram range
- Efficient for small to medium document collections

## Development Tools

| Tool | Purpose |
|------|---------|
| VS Code / PyCharm | IDE for development |
| virtualenv | Environment isolation |
| pip | Package management |

## Limitations

- Does not handle very large document collections efficiently
- No GPU acceleration (not needed for this scale)
- Fixed k topics (no automatic topic number selection)

---

**Last Updated**: 2026-03-23