# Text Classification Pipeline

> A complete text classification pipeline using classical machine learning techniques in R. This project demonstrates how to process raw text data, convert it into numerical features using document-feature matrices, train a Naive Bayes classifier, and evaluate model performance.

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | R |
| Text Processing | quanteda (optional) or base R fallback |
| Machine Learning | quanteda.textmodels NB (optional) or base R multinomial NB |
| Data Manipulation | base R |
| Dataset | 20 Newsgroups (subset) |

---

## Prerequisites

### Required Software

1. **R** (version 4.0 or higher)
   - Download from: https://cran.r-project.org/
   - Verify installation: `R --version`

2. **Optional R Packages** (for quanteda backend):
   - `quanteda` - Text processing and document-feature matrix creation
   - `quanteda.textmodels` - Naive Bayes text model
   - The script runs without these packages using a built-in base R fallback.

### System Requirements

- **OS**: Linux, macOS, or Windows
- **RAM**: Minimum 4GB (8GB recommended for larger datasets)
- **Disk Space**: ~500MB for R installation and packages

---

## Installation

### Step 1: Install R

#### On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install r-base
```

#### On Fedora/RHEL/CentOS:
```bash
sudo dnf install R
```

#### On macOS (using Homebrew):
```bash
brew install r
```

#### On Windows:
Download and run the installer from https://cran.r-project.org/bin/windows/base/

### Step 2: Install Optional R Packages

Open R in your terminal or RStudio, then run:

```r
install.packages(c("quanteda", "quanteda.textmodels"))
```

Or from command line:
```bash
R -e 'install.packages(c("quanteda", "quanteda.textmodels"))'
```

### Step 3: Verify Optional Package Installation

```bash
Rscript -e 'library(quanteda); library(quanteda.textmodels); print("Quanteda backend ready")'
```

---

## Usage

### Quick Start

1. **Navigate to the project directory:**
   ```bash
   cd 20_Text_Classification_Pipeline
   ```

2. **Run the classification pipeline:**
   ```bash
   Rscript text_classification.R
   ```

### Expected Output

```
[1] "Confusion Matrix:"
                    test_labels
predicted_classes  comp.graphics sci.space
  comp.graphics              1         0
  sci.space                  0         1
[1] "Accuracy: 1"
```

---

## Project Structure

```
20_Text_Classification_Pipeline/
├── README.md                 # This file - project documentation
├── RULES.md                # Agent operating rules
├── guide.txt               # Project guide and enhancement ideas
├── text_classification.R   # Main R script - classification pipeline
├── newsgroups.csv          # Sample dataset (20 Newsgroups subset)
├── docs/
│   ├── sdlc.md            # Software Development Lifecycle documentation
│   ├── architecture.md    # System architecture and data flow
│   ├── tech_stack.md      # Technology stack details
│   ├── agent_log.md       # Development session logs
│   ├── CHANGELOG.md       # Version history
│   └── tasks.md           # Task tracking
└── BUILD_LOG.md           # Build process and verification log
```

---

## Architecture Overview

The text classification pipeline follows a standard ML workflow:

```
Raw Text Data
     ↓
[Data Loading] → newsgroups.csv
     ↓
[Text Preprocessing] → quanteda tokens or base-R tokenizer
     ↓
[Tokenization] → Remove punctuation, numbers, stopwords
     ↓
[Feature Extraction] → Document-Feature Matrix (DFM)
     ↓
[Train/Test Split] → 80/20 split
     ↓
[Model Training] → Naive Bayes Classifier
     ↓
[Prediction] → Class labels for test set
     ↓
[Evaluation] → Confusion Matrix + Accuracy
```

### Key Components

1. **Data Layer**: CSV file containing text documents and labels
2. **Preprocessing Layer**: Text cleaning, tokenization, stopword removal
3. **Feature Layer**: Document-Feature Matrix (bag-of-words representation)
4. **Model Layer**: Naive Bayes classifier (quanteda.textmodels or base-R fallback)
5. **Evaluation Layer**: Confusion matrix and accuracy metrics

---

## Environment Variables

This project does not require environment variables. All configuration is handled within the R script.

---

## Running Tests

### Smoke Test

Verify the pipeline runs successfully:

```bash
Rscript text_classification.R
```

Expected: Script completes without errors and outputs confusion matrix with accuracy score.

### Manual Testing

Test with custom data by modifying `newsgroups.csv`:

```csv
text,topic
"Your custom text here","your.category"
"Another example","another.category"
```

---

## SDLC Status

| Phase | Status | Details |
|-------|--------|---------|
| Requirements | ✅ Complete | Documented in docs/sdlc.md |
| Design | ✅ Complete | Architecture documented |
| Development | ✅ Complete | R script implemented |
| Testing | ✅ Complete | Smoke test verified with base R fallback |
| Deployment | ✅ Complete | Ready for use |
| Maintenance | 🔄 Ongoing | See docs/CHANGELOG.md |

**Build Status**: Runtime verified on 2026-03-25 with `Rscript text_classification.R` (`exit=0`) using base R fallback. Optional quanteda backend remains available when packages are installed.

See [docs/sdlc.md](docs/sdlc.md) for full SDLC documentation.

---

## Common Troubleshooting

### Issue: "Rscript: command not found"

**Cause**: R is not installed or not in PATH.

**Solution**:
1. Install R following the Installation section
2. Verify R is in your PATH:
   ```bash
   which R
   which Rscript
   ```
3. If not found, add to PATH:
   ```bash
   export PATH="/usr/local/bin:$PATH"  # Adjust path as needed
   ```

### Issue: "Error: package 'quanteda' not found"

**Cause**: Optional quanteda backend not installed.

**Solution**:
```bash
R -e 'install.packages(c("quanteda", "quanteda.textmodels"))'
```
Or run the script as-is; it will automatically use the built-in base R fallback.

### Issue: "Not enough data to split into training and testing sets"

**Cause**: Dataset has fewer than 2 rows.

**Solution**: Ensure `newsgroups.csv` has at least 5-10 rows for meaningful train/test split.

### Issue: "Error in library(tidyverse): there is no package called 'tidyverse'"

**Cause**: Package installation failed or R library path issue.

**Solution**:
1. Check R library path:
   ```r
   .libPaths()
   ```
2. Install packages with explicit library path:
   ```r
   install.packages("tidyverse", lib="/path/to/R/library")
   ```

### Issue: "Warning: package 'quanteda' was built under R version X.Y.Z"

**Cause**: Version mismatch between R and installed packages.

**Solution**: Update all packages:
```r
update.packages(ask = FALSE)
```

### Issue: Permission denied when installing packages

**Cause**: Insufficient permissions for system R library.

**Solution**: Install to user library:
```r
install.packages(c("tidyverse", "quanteda", "e1071"), lib=Sys.getenv("R_LIBS_USER"))
```

### Issue: "unable to access index for repository" or network errors during package installation

**Cause**: Network restrictions, firewall, or corporate proxy preventing CRAN access.

**Solutions**:

**Option 1: Pre-download packages**
On a machine with internet access:
```bash
# Download source packages
R -e 'download.packages(c("tidyverse", "quanteda", "e1071"), destdir="./r-packages")'
```
Then transfer the `.tar.gz` files and install locally:
```bash
R -e 'install.packages(list.files("./r-packages", pattern="*.tar.gz", full.names=TRUE), repos=NULL, type="source")'
```

**Option 2: Use a different CRAN mirror**
```r
options(repos = c(CRAN = "http://lib.stat.cmu.edu/R/CRAN"))
install.packages(c("tidyverse", "quanteda", "e1071"))
```

**Option 3: Configure proxy settings**
```r
Sys.setenv(http_proxy="http://proxy.company.com:8080")
Sys.setenv(https_proxy="http://proxy.company.com:8080")
install.packages(c("tidyverse", "quanteda", "e1071"))
```

**Option 4: Use Docker**
If you have Docker available:
```dockerfile
FROM rocker/r-ver:latest
RUN install2.r tidyverse quanteda e1071
COPY . /app
WORKDIR /app
CMD ["Rscript", "text_classification.R"]
```

See [BUILD_LOG.md](BUILD_LOG.md) for complete troubleshooting guide and build process documentation.

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes following the coding standards in RULES.md
4. Test your changes: `Rscript text_classification.R`
5. Submit a pull request

---

## License

This project is part of the Super 30 AI/ML learning series.

---

## Additional Resources

- [quanteda documentation](https://quanteda.io/)
- [tidyverse documentation](https://www.tidyverse.org/)
- [e1071 package documentation](https://cran.r-project.org/web/packages/e1071/)
- [20 Newsgroups dataset](http://qwone.com/~jason/20Newsgroups/)

---

**Last Updated**: 2026-03-22  
**Version**: 1.0.0  
**Author**: Ansh
