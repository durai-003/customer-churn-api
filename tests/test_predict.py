def test_predict_valid(client):
    payload = {
        "tenure": 12,
        "Contract": "Month-to-month",
        "InternetService": "Fiber optic",
        "MonthlyCharges": 70.5,
        "TotalCharges": "850.0"
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert data["prediction"] in ["Yes", "No"]

def test_predict_missing_field(client):
    payload = {
        "Contract": "Month-to-month",
        "InternetService": "Fiber optic",
        "MonthlyCharges": 70.5,
        "TotalCharges": "850.0"
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 422

def test_predict_invalid_contract(client):
    payload = {
        "tenure": 12,
        "Contract": "InvalidContract",
        "InternetService": "Fiber optic",
        "MonthlyCharges": 70.5,
        "TotalCharges": "850.0"
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 422