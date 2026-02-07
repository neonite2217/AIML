# BUILD_LOG - Deploy a Machine Learning Model with Docker

Date: 2026-03-17

## Validation Performed
1. Dependency/runtime import check in project venv: PASS
2. Local endpoint smoke test via direct function calls:
   - `predict_price` PASS
   - `predict_price_batch` PASS
3. Docker build attempt: FAILED due host daemon permission
4. Podman container build (Dockerfile-compatible): PASS
5. Podman container runtime + HTTP smoke test: PASS
   - `GET /` returned API banner JSON
   - `POST /predict/` returned numeric prediction JSON

## Commands Executed
```bash
cd 10_Deploy_a_Machine_Learning_Model_with_Docker

./venv/bin/python -c "import fastapi,sklearn,pandas,joblib; print('deps-ok')"

./venv/bin/python - <<'PY'
from main import HousingFeatures, HousingFeaturesBatch, predict_price, predict_price_batch
sample = HousingFeatures(MedInc=8.3252, HouseAge=41.0, AveRooms=6.9841, AveBedrms=1.0238, Population=322.0, AveOccup=2.5556, Latitude=37.88, Longitude=-122.23)
print("single", predict_price(sample))
print("batch", predict_price_batch(HousingFeaturesBatch(features=[sample, sample])))
PY

docker build -t housing-predictor:local .

podman build -t housing-predictor:local .
podman run -d --name project10-test -p 18080:8000 housing-predictor:local
curl -sS http://127.0.0.1:18080/
curl -sS -X POST http://127.0.0.1:18080/predict/ -H 'Content-Type: application/json' \
  -d '{"MedInc":8.3252,"HouseAge":41.0,"AveRooms":6.9841,"AveBedrms":1.0238,"Population":322.0,"AveOccup":2.5556,"Latitude":37.88,"Longitude":-122.23}'
podman rm -f project10-test
```

## Observed Outputs
- Local smoke:
  - `single {'predicted_price': 4.3653}`
  - `batch {'predicted_prices': [4.3653, 4.3653]}`
- Container smoke:
  - `{"message":"California Housing Price Prediction API"}`
  - `{"predicted_price":4.3653}`

## Notes
- Docker daemon access is blocked for this user in this environment:
  - `permission denied while trying to connect to the docker API at unix:///var/run/docker.sock`
- Podman verified that the same `Dockerfile` builds and runs successfully.
- Container logs showed `InconsistentVersionWarning` for scikit-learn model pickle compatibility; prediction still returned successfully.

## Status
- Local app logic: verified
- Containerization workflow: verified via Podman (Docker-compatible OCI runtime)
