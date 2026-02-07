# Build From Scratch - Project 10

This file documents the full reproducible build path used to verify this project.

## 1. Prerequisites
- Python 3
- `pip`
- One OCI runtime:
  - Docker (`docker`) with daemon socket access, or
  - Podman (`podman`) as fallback

## 2. Local Environment Setup
```bash
cd 10_Deploy_a_Machine_Learning_Model_with_Docker
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Local Smoke Test (No Web Server)
```bash
python -c "import fastapi,sklearn,pandas,joblib; print('deps-ok')"
python - <<'PY'
from main import HousingFeatures, HousingFeaturesBatch, predict_price, predict_price_batch
sample = HousingFeatures(MedInc=8.3252, HouseAge=41.0, AveRooms=6.9841, AveBedrms=1.0238, Population=322.0, AveOccup=2.5556, Latitude=37.88, Longitude=-122.23)
print("single", predict_price(sample))
print("batch", predict_price_batch(HousingFeaturesBatch(features=[sample, sample])))
PY
```

Expected output pattern:
- `deps-ok`
- `single {'predicted_price': ...}`
- `batch {'predicted_prices': [..., ...]}`

## 4. Run API Locally
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
Open:
- `http://127.0.0.1:8000/docs`

## 5. Container Build and Run (Preferred: Docker)
```bash
docker build -t housing-predictor:local .
docker run --rm -p 8000:8000 housing-predictor:local
```

## 6. Container Build and Run (Fallback: Podman)
```bash
podman build -t housing-predictor:local .
podman run --rm -p 8000:8000 housing-predictor:local
```

## 7. Container API Verification
```bash
curl -sS http://127.0.0.1:8000/
curl -sS -X POST http://127.0.0.1:8000/predict/ \
  -H 'Content-Type: application/json' \
  -d '{"MedInc":8.3252,"HouseAge":41.0,"AveRooms":6.9841,"AveBedrms":1.0238,"Population":322.0,"AveOccup":2.5556,"Latitude":37.88,"Longitude":-122.23}'
```

Expected output pattern:
- `{"message":"California Housing Price Prediction API"}`
- `{"predicted_price":...}`

## 8. Common Troubleshooting
- Docker socket permission error:
  - `permission denied while trying to connect to the docker API at unix:///var/run/docker.sock`
  - Use Podman fallback commands or request Docker group membership.
- Port conflict:
  - Run on a different port: `uvicorn main:app --port 8001`
- Model version warning in container:
  - Re-export `model.pkl` in the same runtime version as container scikit-learn.
