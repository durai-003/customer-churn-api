from contextlib import asynccontextmanager
from app.models.schemas import PredictionInput

import uuid
import joblib
import pandas as pd
from fastapi import FastAPI

model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model

    model = joblib.load("ml/saved_model/model.joblib")
    print("ML model loaded successfully.")

    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "ML API is alive"}

@app.post("/predict")
def predict(data: PredictionInput):
    sample = pd.DataFrame([{
        "tenure": data.tenure,
        "Contract": data.Contract,
        "InternetService": data.InternetService,
        "MonthlyCharges": data.MonthlyCharges,
        "TotalCharges": data.TotalCharges
    }])

    prediction = model.predict(sample)

    result = "Yes" if prediction[0] == 1 else "No"

    probabilities = model.predict_proba(sample)
    confidence = float(max(probabilities[0]))
    request_id = str(uuid.uuid4())

    return {
    "prediction": result,
    "confidence": confidence,
    "request_id": request_id
}
@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None
    }