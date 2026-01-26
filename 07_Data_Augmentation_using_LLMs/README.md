# Data Augmentation Using LLMs
> Generate structured synthetic tabular data from prompt examples and validate it with a reproducible pipeline.

## Overview
This project demonstrates LLM-based data augmentation to expand small datasets by generating synthetic structured samples following learned patterns. It uses a simulated LLM (pattern-based generator) that learns from example data and generates new rows while maintaining realistic relationships between columns.

## Tech Stack
- Python 3.10+
- pandas (core dependency for data manipulation)
- transformers, torch (listed for future real LLM integration)
- outlines (for structured generation constraints)

## Prerequisites
- Python 3.10 or higher installed
- `pip` package manager available
- Virtual environment support (`python -m venv`)
- Internet connection (for pip package downloads)

## Quick Start

### 1. Clone and Navigate
```bash
cd 07_Data_Augmentation_using_LLMs
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
```

### 3. Activate Virtual Environment
**Linux/macOS:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

### 4. Upgrade pip and Install Dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** The full requirements include heavy packages (torch, transformers). For the simulated script, only pandas is strictly required:
```bash
pip install pandas
```

### 5. Run the Pipeline
```bash
python data_augmentation.py
```

## Expected Output
```
=== STEP 1: Initialize Data Augmentor ===

=== STEP 2: Build Structured Prompt ===
employee_id,years_experience,salary
1,1,50000
2,2,60000
3,3,70000
4,4,80000
5,5,90000

=== STEP 3: Generate Synthetic Data ===
Generated 15 new rows

=== STEP 4: Parse Generated Content into DataFrame ===
Parsed 15 rows into DataFrame
Columns: ['employee_id', 'years_experience', 'salary']

=== STEP 5: VALIDATION ===
✓ Schema valid: ['employee_id', 'years_experience', 'salary']
✓ Type validation passed
✓ Range validation passed
✓ Sanity constraints passed
✓ Duplicates removed: 0

=== RESULTS ===
Total validated rows: 3
Salary range: $59530 - $113248
Experience range: 2 - 4 years

Generated DataFrame:
 employee_id  years_experience  salary
           8                 4  100839
           9                 2   59530
          13                 4  113248

=== STATISTICS ===
Mean salary: $91205.67
Mean experience: 3.33 years
Avg salary per year: $27762.25
```

## Project Structure
```text
07_Data_Augmentation_using_LLMs/
├── data_augmentation.py      # Main implementation of augmentation + validation
├── guide.txt                 # Original lab/project brief
├── BUILD_FROM_SCRATCH.md     # Detailed rebuild/run guide with troubleshooting
├── DEVELOPMENT_LOG.md        # Implementation history and technical decisions
├── requirements.txt          # Dependencies (pandas, transformers, torch, outlines)
├── README.md                 # This file
└── docs/
    └── sdlc.md               # Project SDLC plan and phase tracking
```

## Architecture Overview

### Core Components

1. **DataAugmentor Class** (`data_augmentation.py`)
   - Simulates LLM text generation behavior
   - Learns patterns from example data (salary-to-experience ratio)
   - Generates synthetic rows following learned patterns
   - Uses seeded randomization for reproducibility

2. **5-Step Workflow**
   - **Step 1:** Initialize model/augmentor
   - **Step 2:** Build structured prompt with headers + example rows
   - **Step 3:** Generate synthetic data rows
   - **Step 4:** Parse generated content into Pandas DataFrame
   - **Step 5:** Comprehensive validation pipeline

3. **Validation Pipeline**
   - **Schema validation:** Ensures all expected columns present
   - **Type validation:** Converts and validates numeric types using `pd.to_numeric()`
   - **Range validation:** Filters data within reasonable bounds (0-50 years exp, $30k-$200k salary)
   - **Sanity constraints:** Enforces logical relationships (salary >= experience * $8k)
   - **Duplicate removal:** Uses `df.drop_duplicates()` on employee_id

## SDLC Status
- **Current Phase:** Implementation complete, documentation updated
- **Requirements:** Complete
- **Design:** Complete
- **Implementation:** Complete
- **Testing:** Basic smoke-test level complete
- **Documentation:** Complete
- **Next Phase:** Add automated tests and optional real LLM integration path

Detailed lifecycle plan: [`docs/sdlc.md`](./docs/sdlc.md)

## Troubleshooting

### Common Issues and Solutions

#### Issue: `ModuleNotFoundError: No module named 'pandas'`
**Cause:** Virtual environment not activated or pandas not installed

**Solution:**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate      # Windows

# Install pandas
pip install pandas
```

#### Issue: Slow or heavy install from torch/transformers
**Cause:** These are large packages with many dependencies

**Solution:**
For the simulated script, you only need pandas:
```bash
pip install pandas
```

Keep full requirements for future real-model work.

#### Issue: Script exits early with pandas error
**Cause:** Wrong Python interpreter being used

**Solution:**
```bash
# Confirm interpreter path
which python

# Should show: /path/to/07_Data_Augmentation_using_LLMs/.venv/bin/python

# If not, reactivate virtual environment
source .venv/bin/activate
```

#### Issue: Permission denied when creating virtual environment
**Cause:** Insufficient permissions

**Solution:**
```bash
# Use user-specific installation
python3 -m venv --user .venv
# or
python3 -m venv .venv --without-pip
source .venv/bin/activate
curl https://bootstrap.pypa.io/get-pip.py | python
```

#### Issue: Generated data seems unrealistic
**Cause:** Validation constraints may be too strict or too loose

**Solution:**
Adjust validation parameters in `data_augmentation.py`:
```python
# Line 89-90: Adjust ranges
df = df[(df['years_experience'] >= 0) & (df['years_experience'] <= 50)]
df = df[(df['salary'] >= 30000) & (df['salary'] <= 200000)]

# Line 94: Adjust sanity constraint
df = df[df['salary'] >= (df['years_experience'] * 8000)]
```

#### Issue: No output or empty DataFrame
**Cause:** All rows filtered out by validation

**Solution:**
Check validation constraints are not too strict. Review the validation section in the script output to see which checks are failing.

## Environment Variables
| Name | Required | Description | Default |
|---|---|---|---|
| `PYTHONHASHSEED` | No | Optional deterministic hashing in Python runs | unset |
| `AUGMENT_SEED` | No | Optional custom random seed (if wired into script later) | `42` |

## Running Tests

### Smoke Test
```bash
python data_augmentation.py
```

**Success Criteria:**
- Script exits cleanly (no errors)
- All five workflow stages print
- Validation summary shows at the end
- DataFrame output and statistics are displayed
- At least some rows pass validation (typically 3-8 rows)

### Verification Checklist
- [ ] Virtual environment created and activated
- [ ] Dependencies installed successfully
- [ ] Script runs without import errors
- [ ] All 5 steps execute
- [ ] DataFrame is created with correct columns
- [ ] Validation checks pass
- [ ] Final statistics are calculated and displayed

## Production Considerations

To use with actual GPT-2:

1. **Install full dependencies:**
   ```bash
   pip install transformers torch
   ```

2. **Replace DataAugmentor with real LLM:**
   ```python
   from transformers import pipeline, set_seed
   generator = pipeline('text-generation', model='gpt2')
   set_seed(42)
   ```

3. **Adjust parsing logic** for free-form LLM output (the current script expects CSV-like format)

## Contributing
1. Keep generation deterministic for reproducible reviews
2. Update `DEVELOPMENT_LOG.md` when changing core behavior
3. Document new validation rules in both `README.md` and `docs/sdlc.md`
4. Test changes with `python data_augmentation.py` before committing

## License
Project-level license is not specified. Follow repository owner guidance.

## Additional Resources
- Original project brief: [`guide.txt`](./guide.txt)
- Build instructions: [`BUILD_FROM_SCRATCH.md`](./BUILD_FROM_SCRATCH.md)
- Development history: [`DEVELOPMENT_LOG.md`](./DEVELOPMENT_LOG.md)
- SDLC documentation: [`docs/sdlc.md`](./docs/sdlc.md)
