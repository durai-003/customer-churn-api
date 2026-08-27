from contextlib import asynccontextmanager
from app.models.schemas import PredictionInput,PredictionOutput
from fastapi.responses import JSONResponse

import uuid
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

class PredictionError(Exception):
    pass

model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model

    model = joblib.load("ml/saved_model/model.joblib")
    print("ML model loaded successfully.")

    yield

app = FastAPI(lifespan=lifespan)

@app.exception_handler(PredictionError)
async def prediction_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Prediction failed"}
    )

@app.get("/")
def root():
    return {"message": "ML API is alive"}

@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput):
    sample = pd.DataFrame([{
        "tenure": data.tenure,
        "Contract": data.Contract,
        "InternetService": data.InternetService,
        "MonthlyCharges": data.MonthlyCharges,
        "TotalCharges": data.TotalCharges
    }])

    try:
        prediction = model.predict(sample)
        result = "Yes" if prediction[0] == 1 else "No"
        probabilities = model.predict_proba(sample)
        confidence = float(max(probabilities[0]))

    except Exception:
        raise HTTPException(
        status_code=500,
        detail="Prediction failed"
    )

    request_id = str(uuid.uuid4())

    return {
    "prediction": result,
    "confidence": confidence,
    "model_version": "1.0",
    "request_id": request_id
}
@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None
    }

