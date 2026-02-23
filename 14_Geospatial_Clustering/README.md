# Geospatial Clustering
> Cluster delivery points, detect outliers, compare K-Means vs DBSCAN, and generate route plans.

## Tech Stack
- Python 3.10+
- pandas, numpy
- scikit-learn
- matplotlib
- folium
- pytest

## Prerequisites
- Python 3
- `pip`
- Optional virtual environment support (`python -m venv`)

## Installation
```bash
cd 14_Geospatial_Clustering
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage
Run the full geospatial pipeline:
```bash
MPLCONFIGDIR=/tmp/mpl python geospatial_clustering.py
```

Run tests:
```bash
MPLCONFIGDIR=/tmp/mpl python -m pytest -q
```

## Project Structure
```text
14_Geospatial_Clustering/
├── geospatial_clustering.py      # Main clustering, visualization, and routing pipeline
├── tests/test_clustering.py      # Unit tests for core helpers
├── deliverytime.txt              # Input delivery coordinates
├── clustered_deliveries.csv      # Cleaned + clustered output
├── optimized_routes.csv          # TSP route summary by zone
├── interactive_map.html          # Interactive Folium map output
├── plot_1_raw_locations.png      # Raw point scatter
├── plot_2_elbow_method.png       # K selection chart
├── plot_3_kmeans_clusters.png    # K-Means zone view
├── plot_4_dbscan_clusters.png    # DBSCAN comparison view
├── BUILD_FROM_SCRATCH.md         # Clean setup and run guide
├── BUILD_LOG.md                  # Latest verified build/test notes
├── guide.txt                     # Lab/project brief
├── requirements.txt              # Dependencies
└── docs/
    └── sdlc.md                   # Project SDLC status and plan
```

## Architecture Overview
1. Load coordinate dataset (`deliverytime.txt`).
2. Standardize coordinates and run K-Means (with elbow analysis).
3. Detect/remove outliers using distance-to-centroid IQR thresholds.
4. Label cluster zones and profile cluster density.
5. Compare with DBSCAN.
6. Export CSV/plots/map and optimize route order per zone using nearest-neighbor TSP.

## Environment Variables
| Name | Required | Description | Default |
|---|---|---|---|
| `MPLCONFIGDIR` | Recommended | Writable matplotlib cache path in restricted environments | system default |

## Running Tests
```bash
MPLCONFIGDIR=/tmp/mpl python -m pytest -q
```

Expected:
- helper function tests pass
- no crashes in import path

## SDLC Status
- Current phase: **Verified Implementation + Documentation Complete**
- Details: [`docs/sdlc.md`](./docs/sdlc.md)

## Contributing
1. Keep coordinate transforms and clustering parameters explicit.
2. Preserve deterministic seeds for clustering (`random_state=42`).
3. Update `BUILD_LOG.md` when behavior or outputs change.

## License
Project-level license is not explicitly defined. Follow repository owner guidance.
