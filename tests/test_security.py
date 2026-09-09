def test_missing_api_key(client):
    client.headers.pop("X-API-Key", None)
    payload = {
        "tenure": 12,
        "Contract": "Month-to-month",
        "InternetService": "Fiber optic",
        "MonthlyCharges": 70.5,
        "TotalCharges": 850.0
    }

    response = client.post(
        "/api/v1/predict",
        json=payload
    )

    assert response.status_code == 401


def test_invalid_api_key(client):
    payload = {
        "tenure": 12,
        "Contract": "Month-to-month",
        "InternetService": "Fiber optic",
        "MonthlyCharges": 70.5,
        "TotalCharges": 850.0
    }

    response = client.post(
        "/api/v1/predict",
        json=payload,
        headers={"X-API-Key": "wrong-key"}
    )

    assert response.status_code == 401


def test_unexpected_extra_field(client):
    payload = {
        "tenure": 12,
        "Contract": "Month-to-month",
        "InternetService": "Fiber optic",
        "MonthlyCharges": 70.5,
        "TotalCharges": 850.0,
        "unexpected_field": "not allowed"
    }

    response = client.post(
        "/api/v1/predict",
        json=payload,
        headers={"X-API-Key": "dev-secret-key-123"}
    )

    assert response.status_code == 422
