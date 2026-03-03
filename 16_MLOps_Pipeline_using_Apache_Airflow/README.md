# MLOps Pipeline using Apache Airflow

> A production-grade MLOps pipeline that automates the machine learning lifecycle for screentime analysis, from data preprocessing and model training to evaluation and artifact generation.

## Tech Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Orchestration | Apache Airflow | 3.0.6 | Workflow scheduling and monitoring |
| Language | Python | 3.14+ | ML pipeline implementation |
| ML Framework | scikit-learn | 1.3+ | Model training and evaluation |
| Data Processing | pandas | 2.0+ | Data manipulation |
| Math Library | numpy | 1.24+ | Numerical computations |
| Database | SQLite | - | Airflow metadata storage |

## Prerequisites

Before building and running this project, ensure you have the following:

- **Python 3.14+**
  - Verify: `python --version`
- **pip** (Python package manager)
  - Comes bundled with Python
- **Git** (for cloning the repository)

### System Requirements

- Linux, macOS, or Windows (WSL recommended for Windows)
- At least 4GB RAM (for Airflow webserver and scheduler)
- 1GB disk space (for Airflow database and logs)

## Installation

### Step 1: Navigate to Project Directory

```bash
cd 16_MLOps_Pipeline_using_Apache_Airflow
```

### Step 2: Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

Required packages:
- `apache-airflow>=3.0.0`
- `scikit-learn>=1.3.0`
- `pandas>=2.0.0`

### Step 4: Initialize Airflow

```bash
# Run the setup script (Unix/Linux/macOS)
chmod +x scripts/setup.sh
./scripts/setup.sh

# Or run the setup script (Windows PowerShell)
.\scripts\setup.ps1
```

The setup script will:
1. Create the Airflow home directory structure
2. Initialize the Airflow database
3. Create an admin user
4. Configure the webserver

### Step 5: Verify Installation

```bash
# Check Airflow version
airflow version

# Verify database connection
airflow db check
```

## Usage

### Starting Airflow Services

The pipeline requires both the Airflow scheduler and webserver to run.

**Option 1: Run in Background (Recommended)**

```bash
# Start scheduler in background
airflow scheduler --daemon

# Start webserver in background
airflow webserver --daemon -p 8080
```

**Option 2: Run in Foreground (for debugging)**

Open two terminal windows:

Terminal 1 (Scheduler):
```bash
airflow scheduler
```

Terminal 2 (Webserver):
```bash
airflow webserver -p 8080
```

### Accessing the Airflow UI

Once both services are running:

1. Open your browser and navigate to: `http://localhost:8080`
2. Log in with the credentials created during setup (default: `admin/admin`)
3. You should see the `mlops_pipeline_screentime` DAG in the DAGs list

### Running the Pipeline

**Via Airflow UI:**

1. Locate the `mlops_pipeline_screentime` DAG
2. Toggle the switch to enable it (if not already enabled)
3. Click the "Play" button and select "Trigger DAG"

**Via Command Line:**

```bash
# Trigger the DAG
airflow dags trigger mlops_pipeline_screentime

# Check DAG status
airflow dags list-runs -d mlops_pipeline_screentime

# List tasks in the DAG
airflow tasks list mlops_pipeline_screentime

# Check specific task logs
airflow tasks logs mlops_pipeline_screentime train_and_evaluate
```

### Viewing Pipeline Output

After a successful run, check the generated artifacts:

```bash
# View evaluation metrics (MAE, MSE, R2)
cat artifacts/metrics.json

# View processed dataset
head data/processed_data.csv

# View task logs
cat logs/dag_id=mlops_pipeline_screentime/run_id=*/task_id=train_and_evaluate/*.log
```

**Example metrics.json output:**
```json
{
  "mean_absolute_error": 0.0543,
  "mean_squared_error": 0.0042,
  "root_mean_squared_error": 0.0648,
  "r2_score": 0.9987,
  "n_estimators": 100,
  "test_samples": 20,
  "training_samples": 80
}
```

## Project Structure

```
16_MLOps_Pipeline_using_Apache_Airflow/
├── dags/
│   └── ml_pipeline_dag.py          # Main ML pipeline DAG definition
├── data/                            # Data directory (auto-created)
│   ├── screentime_analysis.csv     # Raw dataset
│   └── processed_data.csv          # Preprocessed dataset
├── artifacts/                       # Output artifacts (auto-created)
│   ├── metrics.json                # Model evaluation metrics
│   └── model.pkl                   # Trained model (if saved)
├── logs/                            # Airflow logs (auto-created)
├── config/                          # Configuration files
│   └── airflow.cfg                 # Airflow configuration
├── scripts/                         # Setup and utility scripts
│   ├── setup.sh                    # Unix/Linux/macOS setup
│   └── setup.ps1                   # Windows PowerShell setup
├── docs/                            # Documentation
│   ├── agent_log.md                # Agent session log
│   ├── architecture.md             # System architecture
│   ├── CHANGELOG.md                # Version history
│   ├── sdlc.md                     # SDLC tracking
│   ├── tasks.md                    # Task backlog
│   └── tech_stack.md               # Technology decisions
├── backups/                         # Backup folder
├── tests/                           # Unit tests (placeholder)
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
└── RULES.md                         # Agent operating rules
```

### File Descriptions

| File | Purpose |
|------|---------|
| `dags/ml_pipeline_dag.py` | DAG definition with data creation, preprocessing, and model training tasks |
| `requirements.txt` | Python package dependencies |
| `scripts/setup.sh` | Automated setup script for Unix systems |
| `scripts/setup.ps1` | Automated setup script for Windows |
| `config/airflow.cfg` | Airflow configuration settings |

## Architecture Overview

This project implements a **3-stage ML pipeline** using Airflow's DAG orchestration:

```
[Data Source]
     │
     ▼
┌─────────────────┐
│  Task 1:        │
│  create_dataset │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐     ┌─────────────────┐
│  Task 2:            │────▶│  Data Quality   │
│  preprocess_data    │     │  Checks         │
└────────┬────────────┘     └─────────────────┘
         │
         ▼
┌──────────────────────────┐     ┌─────────────────┐
│  Task 3:                 │────▶│  Metrics: MAE   │
│  train_and_evaluate      │     │  MSE, R2        │
└────────┬─────────────────┘     └─────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Artifacts Generated    │
│  - metrics.json         │
│  - model.pkl            │
└─────────────────────────┘
```

### Pipeline Stages

1. **Data Creation** (`create_dataset`)
   - Generates synthetic screentime data
   - Creates features: days_since_install, app_usage_hours, user_rating
   - Validates dataset integrity

2. **Preprocessing** (`preprocess_data`)
   - Feature engineering: usage_per_day calculation
   - Missing value imputation
   - StandardScaler normalization
   - Data validation checks

3. **Training & Evaluation** (`train_and_evaluate`)
   - Random Forest Regressor training (100 estimators)
   - 80/20 train-test split
   - MAE, MSE, RMSE, R2 metric calculation
   - Artifact generation and logging

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.

## Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `AIRFLOW_HOME` | Yes | Path to Airflow home directory | `./airflow_home` |
| `AIRFLOW__CORE__EXECUTOR` | No | Task execution backend | `SequentialExecutor` |
| `AIRFLOW__CORE__DAGS_FOLDER` | No | Path to DAGs directory | `./dags` |

### Setting Environment Variables

```bash
# Linux/macOS
export AIRFLOW_HOME=/path/to/project/airflow_home

# Windows (PowerShell)
$env:AIRFLOW_HOME = "C:\path\to\project\airflow_home"
```

## Running Tests

### Smoke Test

Verify the DAG can be loaded and parsed:

```bash
# Validate DAG syntax
python -c "from dags.ml_pipeline_dag import dag; print('DAG loaded successfully')"

# List DAGs
airflow dags list | grep mlops_pipeline_screentime

# Check for DAG import errors
cat logs/dag_processor_manager/dag_processor_manager.log | grep -i error
```

### Manual Testing

```bash
# Trigger a test run
airflow dags trigger mlops_pipeline_screentime

# Monitor task execution
airflow tasks state mlops_pipeline_screentime train_and_evaluate

# Verify artifacts exist
ls -la artifacts/metrics.json
ls -la data/processed_data.csv
```

## SDLC Status

**Current Phase**: Development (v1.0.0)

| Phase | Status | Notes |
|-------|--------|-------|
| Requirements | Completed | ML pipeline requirements defined |
| Design | Completed | DAG architecture documented |
| Development | Completed | Core functionality implemented |
| Testing | Completed | Smoke tests pass, DAG runs successfully |
| Deployment | In Progress | Local deployment configured |
| Maintenance | Started | Documentation complete |

See [docs/sdlc.md](docs/sdlc.md) for full SDLC documentation.

## Troubleshooting

### Installation Issues

#### Error: `pip: command not found`

**Cause**: pip is not installed or not in PATH.

**Solution**:
```bash
# Install pip
python -m ensurepip --upgrade

# Or on Debian/Ubuntu
sudo apt-get install python3-pip
```

#### Error: `No module named 'airflow'`

**Cause**: Airflow not installed or virtual environment not activated.

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate

# Install Airflow
pip install apache-airflow
```

### Airflow Database Issues

#### Error: `database locked` or `SQLite lock`

**Cause**: Concurrent access to SQLite database.

**Solution**:
```bash
# Reset Airflow database
airflow db reset

# Or use a different metadata database in production
```

#### Error: `table alembic_version doesn't exist`

**Cause**: Database not properly initialized.

**Solution**:
```bash
# Initialize database
airflow db migrate
```

### DAG Execution Issues

#### Error: `DAG not found in DagBag`

**Cause**: DAG file has syntax errors or is in wrong location.

**Solution**:
```bash
# Verify DAG file location
ls -la dags/

# Test DAG import
python dags/ml_pipeline_dag.py

# Check DAG processor logs
tail -f logs/dag_processor_manager/dag_processor_manager.log
```

#### Error: `Task instance failed`

**Cause**: Code error in task or missing dependencies.

**Solution**:
```bash
# Check task logs
airflow tasks logs mlops_pipeline_screentime train_and_evaluate

# Run task locally for debugging
airflow tasks test mlops_pipeline_screentime train_and_evaluate 2026-03-25
```

### Performance Issues

#### Slow DAG execution

**Cause**: Default SequentialExecutor processes one task at a time.

**Solution**: For production, configure LocalExecutor or CeleryExecutor:
```bash
# In config/airflow.cfg
executor = LocalExecutor
```

#### Webserver takes too long to start

**Cause**: Large number of DAGs or slow database.

**Solution**:
```bash
# Reduce DAG parsing time
export AIRFLOW__SCHEDULER__MIN_FILE_PROCESS_INTERVAL=30
```

### Common Commands

```bash
# Check Airflow configuration
airflow config get-value core executor

# List all DAGs
airflow dags list

# Trigger DAG manually
airflow dags trigger mlops_pipeline_screentime

# View DAG details
airflow dags show mlops_pipeline_screentime

# Stop background services
pkill -f "airflow scheduler"
pkill -f "airflow webserver"
```

## Future Enhancements

- [ ] Integration with MLflow for experiment tracking
- [ ] Model registry for versioned model storage
- [ ] Data validation with Great Expectations
- [ ] Automated retraining on data drift detection
- [ ] CI/CD pipeline for DAG deployment
- [ ] Unit tests with pytest (>70% coverage)
- [ ] Docker containerization
- [ ] Production deployment guide
- [ ] REST API for pipeline triggers
- [ ] Grafana dashboards for monitoring

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes following Python style guidelines (PEP 8)
4. Test thoroughly: `airflow dags trigger mlops_pipeline_screentime`
5. Commit with descriptive messages
6. Push and create a pull request

### Code Style

- Follow PEP 8 naming conventions
- Use type hints where applicable
- Add docstrings to all functions
- Keep functions focused and small (<50 lines)
- Use logging instead of print statements

## License

This project is for educational purposes. See LICENSE file for details.

## Additional Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [docs/agent_log.md](docs/agent_log.md) - Session log
- [docs/architecture.md](docs/architecture.md) - System architecture
- [BUILD_LOG.md](BUILD_LOG.md) - Build process log

---

**Last Updated**: 2026-03-25
**Version**: 1.0.0
**Maintainer**: MLOps Team
