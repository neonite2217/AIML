# Build From Scratch - Project 07

## Goal
Set up and run the data augmentation pipeline from a clean environment.

## Prerequisites
Before starting, ensure you have:
- Python 3.10 or higher installed
- `pip` package manager available
- Terminal/command line access
- Internet connection for downloading packages
- At least 500MB free disk space (for virtual environment and packages)

## Step-by-Step Build Process

### Step 1: Navigate to Project Directory
```bash
cd 07_Data_Augmentation_using_LLMs
```

### Step 2: Create Virtual Environment
Create an isolated Python environment to avoid conflicts with system packages:

```bash
python3 -m venv .venv
```

**What this does:**
- Creates a `.venv` directory containing a fresh Python installation
- Isolates project dependencies from system Python
- Ensures reproducible builds

**Expected output:**
```
# (no output on success)
```

### Step 3: Activate Virtual Environment

**Linux/macOS:**
```bash
source .venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Verify activation:**
```bash
which python
# Should output: /path/to/07_Data_Augmentation_using_LLMs/.venv/bin/python
```

**Your prompt should change** to show `(.venv)` at the beginning.

### Step 4: Upgrade pip
Ensure you have the latest package manager:

```bash
python -m pip install --upgrade pip
```

**Expected output:**
```
Requirement already satisfied: pip in ./.venv/lib/python3.x/site-packages (xx.x.x)
Collecting pip
  Downloading pip-xx.x.x-py3-none-any.whl
Installing collected packages: pip
Successfully installed pip-xx.x.x
```

### Step 5: Install Dependencies

**Option A: Install all dependencies (for future LLM integration)**
```bash
pip install -r requirements.txt
```

**Option B: Install minimal dependencies (for current simulated script)**
```bash
pip install pandas
```

**Note:** Option A installs heavy packages (torch, transformers) which may take 5-10 minutes and require 2-3GB disk space. Option B is sufficient for the current implementation.

**Expected output (Option B):**
```
Collecting pandas
  Downloading pandas-3.x.x-cp3xx...
Collecting numpy>=2.3.3 (from pandas)
  Downloading numpy-2.x.x...
Collecting python-dateutil>=2.8.2 (from pandas)
  Downloading python_dateutil-2.x.x...
Collecting six>=1.5 (from python-dateutil>=2.8.2->pandas)
  Downloading six-1.x.x...
Installing collected packages: six, numpy, python-dateutil, pandas
Successfully installed numpy-x.x.x pandas-x.x.x python-dateutil-x.x.x six-x.x.x
```

### Step 6: Verify Installation
Check that pandas is installed correctly:

```bash
python -c "import pandas; print(f'pandas {pandas.__version__} installed')"
```

**Expected output:**
```
pandas 3.x.x installed
```

### Step 7: Run the Pipeline
Execute the data augmentation script:

```bash
python data_augmentation.py
```

**Expected output:**
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

## Success Criteria
The build is successful if:
- [ ] Virtual environment created without errors
- [ ] Virtual environment activates successfully
- [ ] pip upgrades without errors
- [ ] Dependencies install without errors
- [ ] Script runs without import errors
- [ ] All 5 steps execute and print
- [ ] Validation checks show ✓ marks
- [ ] Final DataFrame displays with data
- [ ] Statistics are calculated and shown
- [ ] Script exits cleanly (no stack traces)

## Re-run Workflow
After the initial setup, you only need to activate and run:

```bash
source .venv/bin/activate
python data_augmentation.py
```

## Troubleshooting Guide

### Issue: `python3: command not found`
**Symptoms:**
```
bash: python3: command not found
```

**Solutions:**

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3 python3-venv python3-pip
```

**Linux (CentOS/RHEL/Fedora):**
```bash
sudo yum install python3 python3-venv python3-pip
# or
sudo dnf install python3 python3-venv python3-pip
```

**macOS:**
```bash
# Install Homebrew first if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Then install Python
brew install python
```

**Windows:**
Download from https://www.python.org/downloads/windows/

---

### Issue: `ModuleNotFoundError: No module named 'pandas'`
**Symptoms:**
```
WARNING: pandas not installed. Install with: pip install pandas
ERROR: pandas is required for this project
```

**Diagnosis:**
Virtual environment not activated or pandas not installed

**Solutions:**

1. **Check if virtual environment is activated:**
   ```bash
   which python
   # Should show path ending in .venv/bin/python
   ```

2. **Activate if not active:**
   ```bash
   source .venv/bin/activate
   ```

3. **Install pandas:**
   ```bash
   pip install pandas
   ```

4. **Verify installation:**
   ```bash
   pip list | grep pandas
   # Should show: pandas 3.x.x
   ```

---

### Issue: `PermissionError: [Errno 13] Permission denied` when creating venv
**Symptoms:**
```
Error: [Errno 13] Permission denied: '.venv'
```

**Solutions:**

1. **Check directory permissions:**
   ```bash
   ls -la
   # Ensure you have write permissions
   ```

2. **Create in user directory:**
   ```bash
   # Move to a directory you own
   cd ~
   mkdir projects
   cd projects
   # Clone/copy project here, then create venv
   ```

3. **Use --user flag (not recommended for venv):**
   ```bash
   python3 -m venv --user .venv
   ```

---

### Issue: Slow installation / timeout during pip install
**Symptoms:**
```
Connection timed out
ReadTimeoutError
```

**Solutions:**

1. **Use a faster mirror (China users):**
   ```bash
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

2. **Increase timeout:**
   ```bash
   pip install --default-timeout=100 -r requirements.txt
   ```

3. **Install only pandas (minimal):**
   ```bash
   pip install pandas
   ```

4. **Use pre-built wheels:**
   ```bash
   pip install --only-binary :all: pandas
   ```

---

### Issue: Script runs but no rows pass validation
**Symptoms:**
```
Total validated rows: 0
```

**Diagnosis:**
Validation constraints are too strict

**Solutions:**

1. **Check which validation is failing** by adding debug prints to `data_augmentation.py`

2. **Adjust validation ranges** (edit lines 89-90):
   ```python
   # Original (strict):
   df = df[(df['years_experience'] >= 0) & (df['years_experience'] <= 50)]
   df = df[(df['salary'] >= 30000) & (df['salary'] <= 200000)]
   
   # More lenient:
   df = df[(df['years_experience'] >= 0) & (df['years_experience'] <= 100)]
   df = df[(df['salary'] >= 20000) & (df['salary'] <= 500000)]
   ```

3. **Adjust sanity constraint** (edit line 94):
   ```python
   # Original:
   df = df[df['salary'] >= (df['years_experience'] * 8000)]
   
   # More lenient:
   df = df[df['salary'] >= (df['years_experience'] * 5000)]
   ```

---

### Issue: `ImportError: cannot import name 'DataAugmentor'`
**Symptoms:**
```
ImportError: cannot import name 'DataAugmentor' from 'data_augmentation'
```

**Diagnosis:**
Trying to import from the script incorrectly

**Solution:**
This script is meant to be run directly, not imported:
```bash
python data_augmentation.py
```

Not:
```python
from data_augmentation import DataAugmentor  # Don't do this
```

---

### Issue: Virtual environment activates but `which python` shows system Python
**Symptoms:**
```bash
source .venv/bin/activate
which python
# Shows: /usr/bin/python (not the venv path)
```

**Solutions:**

1. **Check shell configuration:**
   Some shells need explicit activation:
   ```bash
   . .venv/bin/activate
   ```

2. **Use full path:**
   ```bash
   .venv/bin/python data_augmentation.py
   ```

3. **Recreate virtual environment:**
   ```bash
   rm -rf .venv
   python3 -m venv .venv
   source .venv/bin/activate
   ```

---

### Issue: `SyntaxError` or `IndentationError`
**Symptoms:**
```
  File "data_augmentation.py", line X
    ^
IndentationError: unexpected indent
```

**Diagnosis:**
File may have been corrupted or edited with wrong editor settings

**Solutions:**

1. **Check file integrity:**
   ```bash
   git checkout data_augmentation.py  # If using git
   ```

2. **Download fresh copy** from repository

3. **Check for tabs vs spaces:**
   ```bash
   cat -A data_augmentation.py | head -20
   # Look for ^I (tabs) - should only see spaces
   ```

---

### Issue: Script hangs / takes too long
**Symptoms:**
Script doesn't complete or seems stuck

**Diagnosis:**
Usually not an issue with this script (it's fast), but could be:
- System under heavy load
- Antivirus scanning Python files
- Network issues (if downloading models)

**Solutions:**

1. **Check system resources:**
   ```bash
   top  # or htop
   ```

2. **Run with timeout:**
   ```bash
   timeout 30 python data_augmentation.py
   ```

3. **Check if it's actually stuck:**
   The script should complete in under 5 seconds. If longer, interrupt with Ctrl+C and check error messages.

---

## Platform-Specific Notes

### Linux
- May need `python3-dev` or `python3-devel` package for some dependencies
- Use `python3` instead of `python` if both are installed
- Virtual environment location: `.venv/bin/`

### macOS
- May need Xcode Command Line Tools: `xcode-select --install`
- Use `python3` from Homebrew
- If using system Python, may need `--user` flag

### Windows
- Use PowerShell or Command Prompt (not Git Bash for venv)
- May need to run as Administrator for some operations
- Virtual environment location: `.venv\Scripts\`
- Use `python` not `python3`

## Verification Commands

After successful build, verify with these commands:

```bash
# Check Python version
python --version

# Check virtual environment
which python

# Check installed packages
pip list

# Check pandas specifically
python -c "import pandas; print(pandas.__version__)"

# Run the script
python data_augmentation.py
```

## Getting Help

If issues persist:

1. **Check documentation:**
   - README.md
   - DEVELOPMENT_LOG.md
   - docs/sdlc.md

2. **Verify environment:**
   ```bash
   python -c "import sys; print(sys.executable)"
   python -c "import pandas; print(pandas.__file__)"
   ```

3. **Clean slate approach:**
   ```bash
   deactivate 2>/dev/null || true
   rm -rf .venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install pandas
   python data_augmentation.py
   ```

## Next Steps

After successful build:

1. **Explore the code:** Open `data_augmentation.py` and understand the 5-step workflow
2. **Modify parameters:** Try changing `num_samples` or validation constraints
3. **Add features:** Implement real LLM integration using transformers
4. **Run tests:** Verify the pipeline works consistently
5. **Read enhancement ideas:** See `guide.txt` section "How you may enhance this project"

## Build Checklist

Use this checklist to track your progress:

- [ ] Python 3.10+ installed
- [ ] Navigated to project directory
- [ ] Virtual environment created (`python3 -m venv .venv`)
- [ ] Virtual environment activated (`source .venv/bin/activate`)
- [ ] pip upgraded (`pip install --upgrade pip`)
- [ ] Dependencies installed (`pip install pandas`)
- [ ] Installation verified (`python -c "import pandas"`)
- [ ] Script runs successfully (`python data_augmentation.py`)
- [ ] All 5 steps execute
- [ ] Validation passes
- [ ] Final statistics displayed
- [ ] No errors in output

**Build Status:** ⬜ In Progress / ⬜ Complete

**Date Completed:** ___________

**Notes:** _______________________________
