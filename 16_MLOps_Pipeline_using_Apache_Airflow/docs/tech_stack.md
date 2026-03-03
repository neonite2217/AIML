# Technology Stack — MLOps Pipeline using Apache Airflow

## Overview

This document outlines the technology choices made for the MLOps Pipeline project, including rationale for each selection and alternatives considered.

---

## Core Technologies

### 1. Apache Airflow (v3.0.6)

**Purpose**: Workflow orchestration and scheduling

**Why Airflow:**
- Industry-standard for data pipeline orchestration
- Rich UI for monitoring and debugging
- Python-based DAGs enable rapid development
- Extensive operator library
- Built-in retry mechanisms
- Task dependency management

**Alternatives Considered:**
- **Prefect**: Simpler, newer but less mature ecosystem
- **Kubeflow Pipelines**: Kubernetes-native, steeper learning curve
- **Luigi**: Spotify's pipeline tool, less active community

**Decision**: Airflow for its maturity, ecosystem, and production readiness.

---

### 2. Python (3.14+)

**Purpose**: Programming language for pipeline implementation

**Why Python:**
- De facto standard for ML/Data Science
- Rich ecosystem (scikit-learn, pandas, numpy)
- Airflow natively supports Python operators
- Type hints for better code quality

**Python Version**: 3.14+
- Latest stable with improved performance
- Type hint enhancements
- Match statements (Python 3.10+)

---

### 3. scikit-learn (v1.3+)

**Purpose**: Machine learning library

**Why scikit-learn:**
- Simple and efficient ML algorithms
- Consistent API across models
- Excellent documentation
- Integration with pandas DataFrames
- Built-in model evaluation metrics

**Model Used**: RandomForestRegressor
- Handles non-linear relationships
- Built-in feature importance
- Robust against overfitting

**Alternatives Considered:**
- **XGBoost**: Higher performance but more complex
- **LightGBM**: Fast training, less interpretability
- **TensorFlow/PyTorch**: Overkill for tabular regression

**Decision**: scikit-learn for simplicity and educational value.

---

### 4. pandas (v2.0+)

**Purpose**: Data manipulation and analysis

**Why pandas:**
- Industry standard for DataFrame operations
- Seamless CSV I/O
- Flexible data transformations
- Integration with scikit-learn

**Key Operations:**
- CSV reading/writing
- Feature engineering (calculated columns)
- Missing value handling
- Data type conversions

---

### 5. numpy (v1.24+)

**Purpose**: Numerical computing

**Why numpy:**
- Efficient array operations
- Mathematical functions (sqrt, etc.)
- Foundation for pandas and scikit-learn

**Usage:**
- RMSE calculation
- Array operations in preprocessing

---

## Infrastructure Stack

### Database: SQLite

**Purpose**: Airflow metadata storage

**Why SQLite:**
- Zero-configuration
- Single file database
- Perfect for local development
- No additional services required

**Production Alternative**: PostgreSQL
- Concurrent access support
- Better performance at scale
- Industry standard for production Airflow

---

### Executor: SequentialExecutor

**Purpose**: Task execution strategy

**Why SequentialExecutor:**
- Default for SQLite backend
- Simple, no additional setup
- Suitable for development

**Production Alternative**: CeleryExecutor or KubernetesExecutor
- Parallel task execution
- Distributed workers
- Horizontal scaling

---

## Development Tools

### Version Control: Git

**Purpose**: Source code management

**Configuration:**
- Repository: Git
- Workflow: Feature branch
- Commit style: Conventional Commits

---

### Package Management: pip

**Purpose**: Python dependency management

**Why pip:**
- Standard Python package manager
- Simple requirements.txt format
- Virtual environment support

**Best Practices:**
- Pin minimum versions, not exact
- Use virtual environments
- Separate dev/prod dependencies

---

## Architecture Decisions

### 1. File-Based Data Storage

**Decision**: Use CSV files for data persistence

**Rationale:**
- Human-readable for debugging
- No database setup required
- Easy to inspect during development

**Trade-offs:**
- Not optimal for large datasets
- No versioning
- Limited query capabilities

**Future**: S3/GCS for production

---

### 2. Sequential Pipeline Execution

**Decision**: Tasks execute sequentially (no parallelism)

**Rationale:**
- Simpler dependency management
- Easier debugging
- Suitable for small datasets

**Future**: Parallel execution with CeleryExecutor

---

### 3. Local Artifact Storage

**Decision**: Store metrics and models locally

**Rationale:**
- Simple setup
- No external service dependencies
- Easy to verify outputs

**Future**: Model Registry (MLflow), Artifact Store (MinIO/S3)

---

## Security Stack

### Authentication: Airflow Default

**Current**: Default Airflow authentication
- Username: `admin`
- Password: `admin` (configurable)

**Future**: LDAP, OAuth, SSO integration

---

## Monitoring Stack

### Current: Airflow Built-in

**Features:**
- Task execution logs
- DAG run history
- Task duration tracking
- SLAs and alerting

**Future Enhancements:**
- Prometheus metrics
- Grafana dashboards
- PagerDuty integration

---

## Technology Versions

| Component | Version | Reason |
|-----------|---------|--------|
| Apache Airflow | 3.0.6 | Latest stable with Python 3.14 support |
| Python | 3.14+ | Latest stable release |
| scikit-learn | 1.3+ | Stable API, good performance |
| pandas | 2.0+ | Performance improvements |
| numpy | 1.24+ | Compatibility with pandas 2.0 |

---

## Compatibility Matrix

| Component | Python 3.12 | Python 3.13 | Python 3.14 |
|-----------|-------------|-------------|-------------|
| Airflow 3.0.6 | ❌ | ❌ | ✅ |
| scikit-learn 1.3 | ✅ | ✅ | ✅ |
| pandas 2.0 | ✅ | ✅ | ✅ |
| numpy 1.24 | ✅ | ✅ | ✅ |

---

## Migration Path

### Development → Production

1. **Phase 1** (Current): Local development
   - SQLite database
   - SequentialExecutor
   - Local file storage

2. **Phase 2** (Future): Staging
   - PostgreSQL database
   - LocalExecutor
   - Local/S3 storage

3. **Phase 3** (Future): Production
   - PostgreSQL + Redis
   - CeleryExecutor
   - S3 artifact store
   - Monitoring stack

---

## Cost Analysis

### Current (Local)

| Component | Cost |
|-----------|------|
| Airflow | $0 (Open Source) |
| SQLite | $0 (Bundled) |
| Compute | $0 (Local machine) |
| **Total** | **$0** |

### Production (Estimated)

| Component | Cost/Month |
|-----------|------------|
| Airflow (EC2) | ~$50-100 |
| PostgreSQL (RDS) | ~$15-30 |
| Redis (ElastiCache) | ~$15-30 |
| S3 Storage | ~$1-5 |
| **Total** | **~$80-165** |

---

## References

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [pandas Documentation](https://pandas.pydata.org/)
- [PEP 8 Style Guide](https://pep8.org/)

---

**Last Updated**: 2026-03-25
**Version**: 1.0.0
**Maintainer**: MLOps Team
