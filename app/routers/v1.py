from fastapi import APIRouter, Request, HTTPException, Depends
from app.security import verify_api_key
from app.models.schemas import (
    PredictionInput,
    PredictionOutput,
    PredictionBatchInput,
    PredictionBatchOutput,
    ModelInfoOutput
)
from app.logging_config import setup_logger
from app.metrics import churn_predictions_total
from app.config import settings
import json
import joblib
import pandas as pd

logger = setup_logger()
router = APIRouter(prefix="/api/v1")
model = None
def load_model():
    global model
    model = joblib.load(settings.MODEL_PATH)
@router.post("/predict", response_model=PredictionOutput)
def predict(
    data: PredictionInput,
    request: Request,
    api_key: str = Depends(verify_api_key)
):
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
        churn_predictions_total.labels(prediction=result).inc()
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
@router.post("/predict-batch", response_model=PredictionBatchOutput)
def predict_batch(data: PredictionBatchInput, request: Request,api_key: str = Depends(verify_api_key)
):
    samples = pd.DataFrame([
        {
            "tenure": item.tenure,
            "Contract": item.Contract,
            "InternetService": item.InternetService,
            "MonthlyCharges": item.MonthlyCharges,
            "TotalCharges": item.TotalCharges
        }
        for item in data.inputs
    ])
    batch_size = len(data.inputs)
    if batch_size > settings.MAX_BATCH_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Batch size cannot exceed {settings.MAX_BATCH_SIZE}"
        )
    logger.info(
        f"batch_prediction_started request_id={request.state.request_id} "
        f"batch_size={batch_size}"
    )
    try:
        predictions = model.predict(samples)
        probabilities = model.predict_proba(samples)
        request_id = request.state.request_id
        results = []
        for index in range(len(data.inputs)):
            result = "Yes" if predictions[index] == 1 else "No"
            confidence = float(max(probabilities[index]))
            results.append({
                "prediction": result,
                "confidence": confidence,
                "model_version": "1.0",
                "request_id": request_id
            })
        logger.info(
            f"batch_prediction_success request_id={request_id} "
            f"batch_size={batch_size}"
        )
        return {
            "predictions": results
        }
    except Exception as e:
        logger.error(
            f"batch_prediction_failed "
            f"request_id={request.state.request_id} "
            f"batch_size={batch_size} "
            f"error={e}"
        )
        raise HTTPException(
            status_code=500,
            detail="Batch prediction failed"
       )
@router.get("/model-info", response_model=ModelInfoOutput)
def model_info(api_key: str = Depends(verify_api_key)
):
    with open("ml/saved_model/model_info.json", "r") as file:
        metadata = json.load(file)
    return metadata
@router.get("/health")
def health(api_key: str = Depends(verify_api_key)
):
    return {
        "status": "ok",
        "model_loaded": model is not None
    }

# API v2 plan:
# If a future /api/v2/predict needs to return extra fields,
# I will create a separate v2 router and separate Pydantic response schema.
# The existing v1 schema and endpoint will remain unchanged
# so existing clients are not broken.   