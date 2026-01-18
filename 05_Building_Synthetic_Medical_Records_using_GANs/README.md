# Synthetic Medical Records GAN - Build Instructions

## Quick Start
```bash
./build.sh
```

## Manual Build
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements_full.txt

# Run full version
python3 medical_gan.py

# Or run demo version (no dependencies)
python3 simple_gan_demo.py
```

## Files
- `medical_gan.py` - Full PyTorch implementation
- `simple_gan_demo.py` - Dependency-free demo
- `build.sh` - Automated build script
- `log.txt` - Build and architecture documentation
- `requirements.txt` - Basic dependencies
- `requirements_full.txt` - Detailed dependencies with versions

## Output
- Synthetic medical records printed to console
- Training progress logged
- Build details in log.txt
