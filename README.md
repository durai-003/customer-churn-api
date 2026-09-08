# ML Model Deployment as a Monitored REST API

## Project Overview

This project focuses on deploying a Machine Learning model as a monitored REST API using FastAPI.

The project uses the Telco Customer Churn dataset to predict whether a customer is likely to churn or not.

## Dataset

This project uses the Telco Customer Churn dataset.

The dataset contains customer information and the target column is `Churn`.

The `Churn` column contains two possible values:

* `Yes` - Customer churned
* `No` - Customer did not churn

## Selected Features

For the MVP, the following five features are selected:

* `tenure`
* `Contract`
* `InternetService`
* `MonthlyCharges`
* `TotalCharges`

## Target

The target variable is `Churn`.

The model will predict whether a customer is likely to churn or not.

## API Endpoint

The prediction API will use the following endpoint:

`POST /predict`

### Request Body

```json
{
  "tenure": 12,
  "Contract": "Month-to-month",
  "InternetService": "Fiber optic",
  "MonthlyCharges": 80.50,
  "TotalCharges": 966.00
}
```

### Response

```json
{
  "prediction": "Yes"
}
```

## Architecture

The application follows this flow:

Client → FastAPI → Validation → ML Model → Prediction → Logging → Response

## Technologies Used

* Python
* FastAPI
* Pydantic
* Uvicorn
* Git
* Docker
* VS Code

## How to Run This Project

### Prerequisites

* Docker Desktop

### Run with Docker Compose

Start the API using:

    docker compose up --build

The API will be available at:

http://localhost:8000

Swagger API documentation:

http://localhost:8000/docs

### Stop the Application

Press Ctrl + C in the terminal running Docker Compose.

To stop and remove the Compose containers and network:

    docker compose down

### Environment Configuration

Environment variables are loaded from the .env file using Docker Compose.

The .env file should contain:

    MODEL_PATH=ml/saved_model/model.joblib
    LOG_LEVEL=INFO
    MAX_BATCH_SIZE=100
    API_TITLE=Customer Churn Prediction API

### Model Volume

The ml/saved_model/ directory is mounted through a named Docker volume. This allows the model files to be managed separately from the application image, so a retrained model can be updated without rebuilding the entire application image.
