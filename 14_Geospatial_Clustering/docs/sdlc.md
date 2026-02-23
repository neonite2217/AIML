# SDLC - Geospatial Clustering

## 1. Requirements
### Functional
- Cluster delivery coordinates into logical zones.
- Detect and exclude spatial outliers.
- Compare K-Means and DBSCAN behavior.
- Produce reusable outputs (CSV, plots, map, route summary).

### Non-Functional
- Reproducible clustering (`random_state=42`).
- Readable outputs for operational planning.
- Script should run on local CPU environment.

## 2. Design
- Single orchestration script (`geospatial_clustering.py`).
- Helper functions exposed for unit testing:
  - `haversine_distance`
  - `nearest_neighbor_tsp`
  - `assign_zone`
- Output-first design: each major stage saves artifacts.

## 3. Implementation
- Implemented staged pipeline from exploration to route optimization.
- Added explicit runtime entrypoint (`if __name__ == "__main__": main()`).
- Existing test suite validates helper correctness.

## 4. Verification
- Smoke run command:
  - `MPLCONFIGDIR=/tmp/mpl ./venv/bin/python geospatial_clustering.py`
- Tests:
  - `MPLCONFIGDIR=/tmp/mpl ./venv/bin/python -m pytest -q`
- Verification status on 2026-03-17:
  - Pipeline run: PASS
  - Tests: PASS (11 passed)

## 5. Deployment / Operational Use
- Local batch analytics workflow.
- Outputs can feed reporting dashboards or planning tools.

## 6. Maintenance
- Keep zone rules and thresholds documented when changed.
- Re-run tests after modifying helper functions.
- Capture updated evidence in `BUILD_LOG.md`.

## 7. Risks and Mitigation
- Risk: environment permission issues for matplotlib cache.
  - Mitigation: set `MPLCONFIGDIR` to writable path (e.g. `/tmp/mpl`).
- Risk: DBSCAN sensitivity to `eps/min_samples`.
  - Mitigation: tune with data snapshots and compare with K-Means baseline.

## 8. Current SDLC Phase (2026-03-17)
- Requirements: Complete
- Design: Complete
- Implementation: Complete
- Verification: Complete
- Documentation: Complete
- Status: Ready / Completed
