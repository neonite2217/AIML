# Architecture — MLOps Pipeline using Apache Airflow

## System Overview

This project implements a production-grade MLOps pipeline for automating the machine learning lifecycle. The system orchestrates data preprocessing, model training, and evaluation using Apache Airflow's DAG (Directed Acyclic Graph) framework.

The pipeline processes screentime analysis data to train a Random Forest Regressor model that predicts user ratings based on app usage patterns.

---

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Airflow Environment                            │
│                                                                          │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────────────┐   │
│  │   Scheduler     │    │   Webserver     │    │   Metadata DB        │   │
│  │   (DAG parsing) │◀──▶│   (UI/API)      │◀──▶│   (SQLite)           │   │
│  └────────┬────────┘    └─────────────────┘    └──────────────────────┘   │
│           │                                                              │
│           ▼                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                     mlops_pipeline_screentime DAG                    │  │
│  │                                                                      │  │
│  │  ┌────────────────┐       ┌────────────────┐       ┌──────────────┐│  │
│  │  │ Task 1:        │──────▶│ Task 2:        │──────▶│ Task 3:      ││  │
│  │  │ create_dataset │       │ preprocess_    │       │ train_and_   ││  │
│  │  │                │       │ data         │       │ evaluate     ││  │
│  │  └────────┬───────┘       └────────┬───────┘       └──────┬───────┘│  │
│  │           │                      │                      │        │  │
│  │           ▼                      ▼                      ▼        │  │
│  │  ┌────────────────┐       ┌────────────────┐       ┌──────────┐ │  │
│  │  │ data/screentime│       │ data/processed │       │ artifacts/ │ │  │
│  │  │ _analysis.csv   │       │ _data.csv      │       │ metrics.   │ │  │
│  │  │                │       │                │       │ json       │ │  │
│  │  └────────────────┘       └────────────────┘       └──────────┘ │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           External Components                            │
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐   │
│  │ scikit-learn     │  │ pandas           │  │ numpy                │   │
│  │ RandomForest     │  │ DataFrame ops    │  │ numerical computing  │   │
│  └──────────────────┘  └──────────────────┘  └──────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. Input Data Generation

```
┌──────────────────────────────────────────────────────────┐
│ create_dataset()                                          │
│                                                          │
│  Generate synthetic data:                                 │
│  - days_since_install: 1-100                             │
│  - app_usage_hours: linear growth                         │
│  - user_rating: 5.0 to 1.0 (decreasing)                  │
│                                                          │
│  Output: data/screentime_analysis.csv                    │
└──────────────────────────────────────────────────────────┘
                           │
                           ▼
```

### 2. Preprocessing Pipeline

```
┌──────────────────────────────────────────────────────────┐
│ preprocess_data()                                         │
│                                                          │
│  Input: screentime_analysis.csv                           │
│                                                          │
│  Transformations:                                         │
│  1. Feature engineering: usage_per_day                  │
│     usage_per_day = app_usage_hours / days_since_install │
│                                                          │
│  2. Missing value imputation                             │
│     fillna(0)                                           │
│                                                          │
│  3. Feature scaling (StandardScaler)                     │
│     mean=0, std=1 for numerical features                 │
│                                                          │
│  Output: data/processed_data.csv                          │
└──────────────────────────────────────────────────────────┘
                           │
                           ▼
```

### 3. Model Training & Evaluation

```
┌──────────────────────────────────────────────────────────┐
│ train_and_evaluate()                                      │
│                                                          │
│  Input: processed_data.csv                               │
│                                                          │
│  Split: 80% train / 20% test                             │
│                                                          │
│  Model: RandomForestRegressor(n_estimators=100)          │
│                                                          │
│  Features: [days_since_install, usage_per_day]          │
│  Target: user_rating                                     │
│                                                          │
│  Metrics:                                                │
│  - MAE (Mean Absolute Error)                             │
│  - MSE (Mean Squared Error)                              │
│  - RMSE (Root Mean Squared Error)                        │
│  - R2 Score                                              │
│                                                          │
│  Output:                                                 │
│  - artifacts/metrics.json                               │
│  - artifacts/model.pkl (if joblib available)              │
└──────────────────────────────────────────────────────────┘
```

---

## Key Design Decisions

### 1. Task Granularity

**Decision**: Split pipeline into 3 distinct tasks (create, preprocess, train)

**Rationale**:
- Enables individual task retry on failure
- Allows for parallel execution of independent tasks (future)
- Provides clear separation of concerns
- Simplifies debugging and monitoring

### 2. Data Persistence Strategy

**Decision**: Use CSV files for intermediate data storage

**Rationale**:
- Human-readable for debugging
- Easy to inspect during pipeline execution
- No external database dependency
- Suitable for small to medium datasets

**Trade-off**: Not optimal for very large datasets or production pipelines with many concurrent runs.

### 3. Model Selection

**Decision**: Random Forest Regressor

**Rationale**:
- Robust against overfitting with small datasets
- Handles non-linear relationships well
- Provides feature importance insights
- Fast training with reasonable accuracy

**Configuration**:
- `n_estimators=100`: Balance between accuracy and training time
- `random_state=42`: Reproducibility

### 4. Metrics Selection

**Decision**: MAE, MSE, RMSE, R2

**Rationale**:
- **MAE**: Easy to interpret (average absolute error)
- **MSE**: Penalizes large errors (sensitive to outliers)
- **RMSE**: Same units as target variable
- **R2**: Explains variance captured by model

### 5. Airflow Configuration

**Decision**: SQLite backend with SequentialExecutor

**Rationale**:
- Simple setup for development and demonstration
- No additional infrastructure required
- Suitable for single-machine deployments

**Future Considerations**:
- PostgreSQL for production
- CeleryExecutor for distributed execution

---

## External Dependencies

| Component | Version | Purpose | Configuration |
|-----------|---------|---------|---------------|
| Apache Airflow | 3.0.6 | Orchestration | SQLite backend, SequentialExecutor |
| scikit-learn | 1.3+ | ML models | RandomForestRegressor |
| pandas | 2.0+ | Data processing | CSV I/O, DataFrame ops |
| numpy | 1.24+ | Numerical ops | Array operations |
| joblib | 1.3+ | Model serialization | Optional dependency |

---

## Security Considerations

1. **No Hardcoded Secrets**: All configuration via environment variables
2. **Local Development Only**: SQLite and SequentialExecutor not for production
3. **Input Validation**: Data validation before processing
4. **No External APIs**: All data is synthetic or local

---

## Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| DAG Parse Time | ~1-2 seconds | Including dependency resolution |
| Task 1 Runtime | ~0.5 seconds | Dataset generation |
| Task 2 Runtime | ~1 second | Preprocessing |
| Task 3 Runtime | ~2-3 seconds | Model training |
| Total Pipeline | ~5 seconds | Sequential execution |
| Memory Usage | ~50-100 MB | Peak during model training |
| Disk Usage | ~10 KB | Small CSV files |

---

## Monitoring & Observability

### Logging
- Task-level logging to Airflow logs
- Metrics written to JSON artifacts
- Execution timestamps via Airflow metadata

### Metrics
- Model performance metrics (MAE, MSE, RMSE, R2)
- Data shape at each stage
- Training/test sample counts

### Alerting (Future)
- MAE threshold monitoring
- Data drift detection
- Pipeline failure notifications

---

## Scalability Considerations

### Current Limitations
- Single-machine execution
- Sequential task processing
- Local file storage

### Scaling Path
1. **Horizontal Scaling**: Migrate to CeleryExecutor with Redis/RabbitMQ
2. **Database**: Switch to PostgreSQL for metadata
3. **Storage**: Use S3/GCS for artifacts
4. **Compute**: KubernetesExecutor for containerized tasks

---

## Future Architecture Enhancements

```
┌─────────────────────────────────────────────────────────────┐
│                     Production Pipeline                    │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ Data Ingest │───▶│ Validation  │───▶│ Feature     │     │
│  │ (Streaming)│    │ (Great      │    │ Store       │     │
│  │             │    │ Expectations)│   │             │     │
│  └─────────────┘    └─────────────┘    └──────┬──────┘     │
│                                                │            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────▼──────┐      │
│  │ Model       │◀───│ Training    │◀───│ Preprocess │      │
│  │ Registry    │    │ (GPU)       │    │             │      │
│  │ (MLflow)    │    │             │    │             │      │
│  └──────┬──────┘    └─────────────┘    └─────────────┘      │
│         │                                                   │
│  ┌──────▼──────┐    ┌─────────────┐    ┌─────────────┐    │
│  │ Deployment  │───▶│ Monitoring  │───▶│ Drift       │    │
│  │ (REST API)  │    │ (Prometheus)│    │ Detection   │    │
│  │             │    │             │    │             │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

*Last Updated: 2026-03-25*
*Version: 1.0.0*
