# Lab Project: Deploy a Machine Learning Model with Docker

from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel
from typing import List
import os
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import GradientBoostingRegressor

app = FastAPI(title="California Housing Price Prediction API")


def create_model():
    model_filename = "model.pkl"
    if not os.path.exists(model_filename):
        print("Training model...")
        housing = fetch_california_housing()
        X = pd.DataFrame(housing.data[:500], columns=housing.feature_names)
        y = housing.target[:500]
        model = GradientBoostingRegressor()
        model.fit(X, y)
        joblib.dump(model, model_filename)
        print("Model saved.")


create_model()
model = joblib.load("model.pkl")


class HousingFeatures(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float


class HousingFeaturesBatch(BaseModel):
    features: List[HousingFeatures]


@app.get("/")
def read_root():
    return {"message": "California Housing Price Prediction API"}


@app.post("/predict/")
def predict_price(features: HousingFeatures):
    data = pd.DataFrame([features.dict()])
    data = data[model.feature_names_in_]
    prediction = model.predict(data)[0]
    return {"predicted_price": float(round(float(prediction), 4))}


@app.post("/predict_batch/")
def predict_price_batch(batch: HousingFeaturesBatch):
    data = pd.DataFrame([f.dict() for f in batch.features])
    data = data[model.feature_names_in_]
    predictions = model.predict(data)
    return {"predicted_prices": [float(round(float(p), 4)) for p in predictions.tolist()]}
