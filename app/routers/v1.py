from fastapi import APIRouter, Request, HTTPException
from app.models.schemas import PredictionInput, PredictionOutput

import joblib
import pandas as pd

router = APIRouter(prefix="/api/v1")

model = None


def load_model():
    global model
    model = joblib.load("ml/saved_model/model.joblib")


@router.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput, request: Request):
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

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )

    request_id = request.state.request_id

    return {
        "prediction": result,
        "confidence": confidence,
        "model_version": "1.0",
        "request_id": request_id
    }


@router.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None
    }

# API v2 plan:
# If a future /api/v2/predict needs to return extra fields,
# I will create a separate v2 router and separate Pydantic response schema.
# The existing v1 schema and endpoint will remain unchanged
# so existing clients are not broken.