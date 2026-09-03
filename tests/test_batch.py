def test_predict_batch_oversized(client, monkeypatch):
    from app.config import settings
    monkeypatch.setattr(settings, "MAX_BATCH_SIZE", 2)
    payload = {
        "inputs": [
            {
                "tenure": 12,
                "Contract": "Month-to-month",
                "InternetService": "Fiber optic",
                "MonthlyCharges": 70.5,
                "TotalCharges": "850.0"
            },
            {
                "tenure": 24,
                "Contract": "One year",
                "InternetService": "DSL",
                "MonthlyCharges": 60.0,
                "TotalCharges": "1400.0"
            },
            {
                "tenure": 36,
                "Contract": "Two year",
                "InternetService": "DSL",
                "MonthlyCharges": 55.0,
                "TotalCharges": "2000.0"
            }
        ]
    }
    response = client.post("/api/v1/predict-batch", json=payload)
    assert response.status_code == 400
    assert "Batch size cannot exceed 2" in response.json()["detail"]