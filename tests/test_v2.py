def test_v1_and_v2_response_shapes(client):
    payload = {
        "tenure": 12,
        "Contract": "Month-to-month",
        "InternetService": "Fiber optic",
        "MonthlyCharges": 70.5,
        "TotalCharges": 850.0
    }

    v1_response = client.post("/api/v1/predict", json=payload)
    v2_response = client.post("/api/v2/predict", json=payload)

    assert v1_response.status_code == 200
    assert v2_response.status_code == 200

    v1_data = v1_response.json()
    v2_data = v2_response.json()

    assert v1_data["prediction"] == v2_data["prediction"]

    assert "probabilities" not in v1_data
    assert v1_data["model_version"] == "1.0"

    assert "probabilities" in v2_data
    assert v2_data["model_version"] == "2.0"

    assert "No" in v2_data["probabilities"]
    assert "Yes" in v2_data["probabilities"]
    
    total_probability = sum(v2_data["probabilities"].values())
    assert abs(total_probability - 1.0) < 0.001