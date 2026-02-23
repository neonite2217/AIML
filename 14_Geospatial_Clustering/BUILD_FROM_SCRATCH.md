# Build From Scratch - Project 14

## 1. Clean Setup
```bash
cd 14_Geospatial_Clustering
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Run Pipeline
```bash
MPLCONFIGDIR=/tmp/mpl python geospatial_clustering.py
```

## 3. Run Tests
```bash
MPLCONFIGDIR=/tmp/mpl python -m pytest -q
```

## 4. Expected Artifacts
- `clustered_deliveries.csv`
- `optimized_routes.csv`
- `interactive_map.html`
- `plot_1_raw_locations.png`
- `plot_2_elbow_method.png`
- `plot_3_kmeans_clusters.png`
- `plot_4_dbscan_clusters.png`

## 5. Common Issues
- Matplotlib cache permission warning:
  - Use `MPLCONFIGDIR=/tmp/mpl` before Python commands.
- Missing package import errors:
  - Ensure virtual environment is active and rerun `pip install -r requirements.txt`.
