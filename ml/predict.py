import joblib
import pandas as pd

model_path = "ml/saved_model/model.joblib"

model = joblib.load(model_path)

sample = pd.DataFrame([{
    "tenure": 12,
    "Contract": "Month-to-month",
    "InternetService": "Fiber optic",
    "MonthlyCharges": 70.0,
    "TotalCharges": 840.0
}])

prediction = model.predict(sample)

print("Prediction:", prediction[0])

if prediction[0] == 1:
    print("Customer is likely to churn.")
else:
    print("Customer is not likely to churn.")