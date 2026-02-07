# Deploy a Machine Learning Model with Docker
> Serve a scikit-learn housing price model through FastAPI and run it locally or in a container.

## Tech Stack
- Python 3.10+
- FastAPI + Uvicorn
- scikit-learn, pandas, joblib
- Dockerfile-compatible OCI containers (`docker` or `podman`)

## Prerequisites
- Python 3
- `pip`
- One container runtime:
  - Docker daemon access (`docker`)
  - or Podman (`podman`) as a Docker-compatible fallback

## Installation
```bash
cd 10_Deploy_a_Machine_Learning_Model_with_Docker
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage
### Getting Started (Local, 5 Minutes)
1. Start the API:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
2. Open interactive docs: `http://127.0.0.1:8000/docs`
3. Quick prediction check:
```bash
curl -sS -X POST http://127.0.0.1:8000/predict/ \
  -H 'Content-Type: application/json' \
  -d '{"MedInc":8.3252,"HouseAge":41.0,"AveRooms":6.9841,"AveBedrms":1.0238,"Population":322.0,"AveOccup":2.5556,"Latitude":37.88,"Longitude":-122.23}'
```

### Container Build and Run (Docker)
```bash
docker build -t housing-predictor:local .
docker run --rm -p 8000:8000 housing-predictor:local
```

### Container Build and Run (Podman Fallback)
```bash
podman build -t housing-predictor:local .
podman run --rm -p 8000:8000 housing-predictor:local
```

## Project Structure
```text
10_Deploy_a_Machine_Learning_Model_with_Docker/
├── main.py                   # FastAPI app with single + batch prediction endpoints
├── model.pkl                 # Trained GradientBoostingRegressor artifact
├── Dockerfile                # Container build definition
├── requirements.txt          # Python dependencies
├── BUILD_FROM_SCRATCH.md     # End-to-end build and verification guide
├── BUILD_LOG.md              # Build/run evidence and verification outputs
├── guide.txt                 # Lab project brief
└── docs/
    └── sdlc.md               # SDLC status and lifecycle plan
```

## Architecture Overview
1. App startup checks for `model.pkl` and trains a fallback model if missing.
2. API endpoints:
   - `GET /` health/info endpoint
   - `POST /predict/` single inference
   - `POST /predict_batch/` batch inference
3. Incoming JSON is validated with Pydantic models.
4. Inference features are aligned to model feature order before prediction.
5. API runs via Uvicorn and is packaged through `Dockerfile`.

## Environment Variables
| Name | Required | Description | Default |
|---|---|---|---|
| `HOST` | No | Uvicorn bind host | `0.0.0.0` |
| `PORT` | No | Uvicorn bind port | `8000` |

## Running Tests
### Python smoke test (no server)
```bash
python - <<'PY'
from main import HousingFeatures, HousingFeaturesBatch, predict_price, predict_price_batch
sample = HousingFeatures(MedInc=8.3252, HouseAge=41.0, AveRooms=6.9841, AveBedrms=1.0238, Population=322.0, AveOccup=2.5556, Latitude=37.88, Longitude=-122.23)
print("single", predict_price(sample))
print("batch", predict_price_batch(HousingFeaturesBatch(features=[sample, sample])))
PY
```

### Container smoke test
```bash
podman run --rm -p 8000:8000 housing-predictor:local
```
Then call:
```bash
curl -sS http://127.0.0.1:8000/
```

## SDLC Status
- Current phase: **Verification and documentation complete**
- Last verified: **2026-03-17**
- Build/run evidence: [`BUILD_LOG.md`](./BUILD_LOG.md)
- SDLC detail: [`docs/sdlc.md`](./docs/sdlc.md)

## Troubleshooting
- `permission denied while trying to connect to docker.sock`:
  - Current user is missing Docker daemon permissions. Use Podman commands above or request Docker group access.
- `InconsistentVersionWarning` for scikit-learn when loading `model.pkl`:
  - Re-train/re-export `model.pkl` inside the target runtime or pin compatible scikit-learn versions.
- API fails to start because port is occupied:
  - Run on another port, e.g. `uvicorn main:app --port 8001`.
- `ModuleNotFoundError` during startup:
  - Re-activate virtual environment and reinstall:
    - `source .venv/bin/activate && pip install -r requirements.txt`

## Contributing
1. Keep endpoint schema backward-compatible.
2. Ensure outputs are JSON-native Python types.
3. Update `BUILD_LOG.md` and `docs/sdlc.md` after every verification run.

## License
Project-level license is not explicitly defined. Follow repository owner guidance.
