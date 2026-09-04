from fastapi import APIRouter, Request, HTTPException
from app.models.schemas import PredictionInput, PredictionV2Output
from app.config import settings
import joblib
import pandas as pd

router = APIRouter(prefix="/api/v2")
model = None
def load_model():
    global model
    model = joblib.load(settings.MODEL_PATH)

@router.post("/predict", response_model=PredictionV2Output)
def predict_v2(data: PredictionInput, request: Request):
    sample = pd.DataFrame([{
        "tenure": data.tenure,
        "Contract": data.Contract,
        "InternetService": data.InternetService,
        "MonthlyCharges": data.MonthlyCharges,
        "TotalCharges": data.TotalCharges
    }])

    try:
        prediction = model.predict(sample)
        probabilities = model.predict_proba(sample)[0]
        result = "Yes" if prediction[0] == 1 else "No"
        confidence = float(max(probabilities))
        probability_distribution = {
            "No": float(probabilities[0]),
            "Yes": float(probabilities[1])
        }
        return {
            "prediction": result,
            "confidence": confidence,
            "probabilities": probability_distribution,
            "model_version": "2.0",
            "request_id": request.state.request_id
        }
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )