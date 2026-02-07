# SDLC - Deploy a Machine Learning Model with Docker

## 1. Requirements
### Functional
- Expose trained ML model through API endpoint(s).
- Support single and batch predictions.
- Containerize application with Docker.

### Non-Functional
- Portable runtime across environments.
- JSON-serializable API responses.
- Reproducible build workflow.

## 2. Design
- FastAPI app in `main.py`.
- Pre-trained model artifact `model.pkl` loaded at startup.
- Dockerfile builds self-contained image including model artifact.

## 3. Implementation
- `/predict/` and `/predict_batch/` implemented.
- Response serialization hardened to Python `float` values.
- Dockerfile updated to include `model.pkl`.

## 4. Verification
Verified on 2026-03-17:
- Local dependency import check: PASS
- Local endpoint function smoke test (direct call): PASS
- Docker build attempt: FAIL (daemon permission on `/var/run/docker.sock`)
- Podman build of same Dockerfile: PASS
- Podman run + endpoint smoke checks: PASS

## 5. Deployment
- Primary deployment path: Docker container + Uvicorn.
- Validation fallback used in this environment: Podman (Dockerfile-compatible OCI runtime).
- Production recommendation: ensure Docker daemon access or use Podman in rootless mode.

## 6. Maintenance
- Keep model schema/feature ordering stable.
- Validate both single and batch paths after model changes.
- Update `BUILD_LOG.md` after each runtime verification.

## 7. Risks and Mitigation
- Risk: Docker daemon access unavailable.
  - Mitigation: coordinate Docker group access; use Podman fallback for local validation.
- Risk: non-JSON types in API responses.
  - Mitigation: explicit float casting in endpoint outputs.
- Risk: model pickle version mismatch with scikit-learn runtime.
  - Mitigation: rebuild `model.pkl` using the target runtime version.

## 8. Current SDLC Phase (2026-03-17)
- Requirements: Complete
- Design: Complete
- Implementation: Complete
- Verification: Complete (Docker path permission-limited, OCI container path validated via Podman)
- Documentation: Complete
- Status: Completed
