from pydantic import BaseModel, Field
from typing import Literal, List

class PredictionInput(BaseModel):
    tenure: int = Field(
        ...,
        ge=0,
        le=100,
        description="Customer tenure in months"
    )
    Contract: Literal["Month-to-month", "One year", "Two year"]
    InternetService: Literal["DSL", "Fiber optic", "No"]
    MonthlyCharges: float = Field(
        ...,
        gt=0,
        description="Monthly charges must be positive"
    )
    TotalCharges: float = Field(
        ...,
        ge=0,
        description="Total charges cannot be negative"
    )

class PredictionOutput(BaseModel):
    prediction: str
    confidence: float
    model_version: str
    request_id: str

class PredictionBatchInput(BaseModel):
    inputs: List[PredictionInput] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="List of 1 to 100 customer inputs"
    )

class PredictionBatchOutput(BaseModel):
    predictions: List[PredictionOutput]


class ModelInfoOutput(BaseModel):
    model_type: str
    version: str
    training_date: str
    features: List[str]