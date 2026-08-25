from pydantic import BaseModel, Field
from typing import Literal

class PredictionInput(BaseModel):
    tenure:int = Field(..., ge=0, le=100, description="Customer tenure in months")
    Contract: Literal["Month-to-month", "One year", "Two year"]
    InternetService: Literal["DSL","Fiber optic","No"]
    MonthlyCharges: float = Field(..., gt=0, description="Monthly charges must be positive")
    TotalCharges: float = Field(...,ge=0, description="Total charges cannot be negative")
