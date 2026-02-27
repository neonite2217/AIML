# SDLC - Hybrid Machine Learning Models

## 1. Requirements
### Functional
- Build sequence-based LSTM forecaster for time-series signal.
- Build lag-feature linear regression forecaster.
- Combine both predictions into a hybrid ensemble.
- Export prediction outputs.

### Non-Functional
- CPU-friendly execution.
- Deterministic behavior through seeding.
- Robust operation with small datasets.

## 2. Design
- Single orchestration script: `hybrid_model.py`.
- Two-model design:
  - nonlinear temporal branch (LSTM)
  - linear trend/lag branch (LinearRegression)
- Ensemble strategy: arithmetic mean of aligned predictions.

## 3. Implementation
- Replaced TensorFlow dependency path with PyTorch LSTM for environment compatibility.
- Added dynamic LSTM time-step selection for short datasets.
- Added CSV export of aligned model predictions.

## 4. Verification
Verified on 2026-03-17:
- `python hybrid_model.py` -> PASS
- Created `hybrid_predictions.csv`
- Printed LSTM/linear/hybrid prediction samples

## 5. Deployment / Runtime
- Local script execution workflow.
- Output CSV can be consumed by downstream analysis/reporting.

## 6. Maintenance
- Keep feature engineering (lag columns) and sequence window logic synchronized.
- Revalidate output alignment whenever changing time-step behavior.

## 7. Risks and Mitigation
- Risk: tiny datasets can break fixed-window sequence generation.
  - Mitigation: dynamic `effective_time_step`.
- Risk: branch misalignment between LSTM and linear outputs.
  - Mitigation: explicit min-length alignment before ensembling.

## 8. Current SDLC Phase (2026-03-17)
- Requirements: Complete
- Design: Complete
- Implementation: Complete
- Verification: Complete
- Documentation: Complete
- Status: Ready / Completed
