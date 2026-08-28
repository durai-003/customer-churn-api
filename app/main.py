from contextlib import asynccontextmanager
from app.models.schemas import PredictionInput,PredictionOutput
from app.logging_config import setup_logger
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Request

import uuid
import time
import joblib
import pandas as pd

class PredictionError(Exception):
    pass

logger = setup_logger()

model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model

    model = joblib.load("ml/saved_model/model.joblib")
    logger.info("ML model loaded successfully.")

    yield

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        f"request_id={request_id} "
        f"method={request.method} "
        f"path={request.url.path} "
        f"duration={duration:.4f}s"
    )

    return response

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
        # prediction = model.predict_broken(sample)
        result = "Yes" if prediction[0] == 1 else "No"
        probabilities = model.predict_proba(sample)
        confidence = float(max(probabilities[0]))

    except Exception as e:
        logger.error(
            f"prediction_failed request_id={request.state.request_id} error={e}"
        )
        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )

    request_id = request.state.request_id
    logger.info(
    f"prediction_success request_id={request_id} prediction={result}"
)

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

