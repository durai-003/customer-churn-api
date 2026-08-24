from contextlib import asynccontextmanager

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
def predict():
    sample = pd.DataFrame([{
        "tenure": 12,
        "Contract": "Month-to-month",
        "InternetService": "Fiber optic",
        "MonthlyCharges": 80.50,
        "TotalCharges": 966.00
    }])

    prediction = model.predict(sample)

    result = "Yes" if prediction[0] == 1 else "No"

    return {"prediction": result}