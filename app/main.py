from contextlib import asynccontextmanager
from app.config import settings
from app.logging_config import setup_logger
from app.routers.v1 import router as v1_router, load_model
from app.routers.v2 import router as v2_router, load_model as load_model_v2
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request

import uuid
import time

class PredictionError(Exception):
    pass

logger = setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    load_model_v2()
    logger.info("ML models loaded successfully.")

    yield
app = FastAPI(
    title=settings.API_TITLE,
    lifespan=lifespan
)

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

app.include_router(v1_router)
app.include_router(v2_router)

# V2 plan:
# If we introduce /api/v2/predict, we will keep the v1 contract unchanged.
# V2 can use a separate Pydantic schema and return additional fields
# without breaking existing v1 clients.