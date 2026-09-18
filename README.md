# ML Model Deployment as a Monitored REST API

## Project Overview

This project focuses on deploying a Machine Learning model as a monitored REST API using FastAPI.

The project uses the Telco Customer Churn dataset to predict whether a customer is likely to churn or not.

The API provides:

- Customer churn prediction
- Batch prediction
- Model information
- API versioning
- Input validation
- API key security
- Structured request logging
- Prometheus monitoring
- Docker and Docker Compose support
- Automated testing

## Dataset

This project uses the Telco Customer Churn dataset.

The dataset contains customer information and the target column is `Churn`.

The `Churn` column contains two possible values:

- `Yes` - Customer churned
- `No` - Customer did not churn

## Selected Features

For the MVP, the following five features are selected:

- `tenure`
- `Contract`
- `InternetService`
- `MonthlyCharges`
- `TotalCharges`

## Target

The target variable is `Churn`.

The model predicts whether a customer is likely to churn or not.

## Machine Learning Model

A machine learning pipeline is trained using the selected customer features.

The trained model is saved using Joblib and loaded by the FastAPI application when the API starts.

The saved model is located at:

```text
ml/saved_model/model.joblib
```

## Architecture

```text
Client
  ↓
FastAPI
  ↓
Request Validation
  ↓
API v1 / API v2
  ↓
ML Model
  ↓
Prediction
  ↓
Logging + Prometheus Metrics
  ↓
Response
```
## API Endpoints
## Root
GET /

Example:

curl http://localhost:8000/

Example response:

{
  "message": "ML API is alive"
}

## Health Check
GET /health

Example:

curl http://localhost:8000/health

Example response:

{
  "status": "healthy"
}

## API v1 Prediction
POST /api/v1/predict

Requires the X-API-Key header.

Example:

curl -X POST http://localhost:8000/api/v1/predict ^
  -H "Content-Type: application/json" ^
  -H "X-API-Key: your-secret-api-key" ^
  -d "{\"tenure\":12,\"Contract\":\"Month-to-month\",\"InternetService\":\"Fiber optic\",\"MonthlyCharges\":80.50,\"TotalCharges\":966.00}"

Example response:

{
  "prediction": "No",
  "confidence": 0.86,
  "model_version": "1.0",
  "request_id": "example-request-id"
}

## API v1 Batch Prediction
POST /api/v1/predict-batch

Requires the X-API-Key header.

Example request:

{
  "inputs": [
    {
      "tenure": 12,
      "Contract": "Month-to-month",
      "InternetService": "Fiber optic",
      "MonthlyCharges": 80.50,
      "TotalCharges": 966.00
    },
    {
      "tenure": 36,
      "Contract": "Two year",
      "InternetService": "DSL",
      "MonthlyCharges": 60.00,
      "TotalCharges": 2160.00
    }
  ]
}

## API v1 Model Information
GET /api/v1/model-info

Requires the X-API-Key header.

This endpoint returns information about the trained model, including its version, training date, model type, and features.

## API v1 Health
GET /api/v1/health

Requires the X-API-Key header.

This endpoint checks whether the API v1 model is loaded.

## API v2 Prediction
POST /api/v2/predict

Requires the X-API-Key header.

API v2 provides the prediction along with the probability distribution for both No and Yes.

Example response:

{
  "prediction": "No",
  "confidence": 0.86,
  "probabilities": {
    "No": 0.86,
    "Yes": 0.14
  },
  "model_version": "2.0",
  "request_id": "example-request-id"
}

## Prometheus Metrics
GET /metrics

Example:

curl http://localhost:8000/metrics

The metrics endpoint exposes API and prediction metrics for monitoring with Prometheus.

## API Documentation

Swagger UI is available at:

http://localhost:8000/docs

OpenAPI JSON:

http://localhost:8000/openapi.json

## Technologies Used
Python
FastAPI
Pydantic
Pandas
Scikit-learn
Joblib
Uvicorn
Pytest
HTTPX
Prometheus
Docker
Docker Compose
Git
GitHub
VS Code

## Project Structure
customer-churn-api/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── security.py
│   ├── metrics.py
│   ├── logging_config.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   └── routers/
│       ├── v1.py
│       └── v2.py
│
├── data/
│   └── Telco-Customer-Churn.csv
│
├── ml/
│   ├── train.py
│   ├── predict.py
│   └── saved_model/
│       ├── model.joblib
│       └── model_info.json
│
├── tests/
│   ├── conftest.py
│   └── ...
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── .gitignore
├── requirements.txt
├── load_test.py
├── TESTING.md
└── README.md

## How to Run This Project
Prerequisites

Install the following:

Docker Desktop
Git

Docker Desktop must be running before starting the application.

## Clone the Repository
git clone https://github.com/durai-003/customer-churn-api.git
cd customer-churn-api

## Environment Configuration

Create a .env file in the project root.

Example:

MODEL_PATH=ml/saved_model/model.joblib
LOG_LEVEL=INFO
MAX_BATCH_SIZE=100
API_TITLE=Customer Churn Prediction API
API_KEY=your-secret-api-key

The .env file is not committed to Git because it can contain secrets.

An example configuration is provided in:

.env.example

## Run with Docker Compose

Build and start the application:

docker compose up --build

The API will be available at:

http://localhost:8000

Swagger API documentation:

http://localhost:8000/docs

Prometheus metrics:

http://localhost:8000/metrics

## Run in Background

To start the application in detached mode:

docker compose up -d --build

## Stop the Application

To stop the running containers:

docker compose down

## Configuration

The application uses environment variables for configuration.

Available settings include:

Variable     	              Description	                                  Example
MODEL_PATH	          Path to the trained model	                ml/saved_model/model.joblib
LOG_LEVEL	            Application logging level	                    INFO
MAX_BATCH_SIZE	      Maximum number of batch inputs	              100
API_TITLE	             FastAPI application title	              Customer Churn Prediction API
API_KEY	API            authentication key	                      your-secret-api-key

## Security

The prediction endpoints are protected using an API key.

The API key must be provided using the following HTTP header:

X-API-Key

Example:

X-API-Key: your-secret-api-key

Requests without a valid API key receive an authentication error.

The actual API key should be stored in .env and should not be committed to Git.

## Input Validation

The API validates incoming customer data using Pydantic.

Validation includes:

tenure must be between 0 and 100
Contract must be one of the supported contract types
InternetService must be one of the supported service types
MonthlyCharges must be greater than 0
TotalCharges cannot be negative
Unexpected additional fields are rejected
Batch requests are limited by MAX_BATCH_SIZE

## Logging and Monitoring

The API includes structured request logging.

Each request receives a unique request_id.

The logs include information such as:

Request ID
HTTP method
Request path
Request duration
Batch prediction information
Prediction success or failure

Prometheus metrics are exposed through:

GET /metrics

The application also tracks successful churn predictions using the:

churn_predictions_total

metric.

## Automated Testing

The project uses Pytest for automated testing.

Run the test suite with:

pytest

The project test suite covers API behavior, validation, authentication, predictions, and related functionality.

The final test suite passed successfully during the project review.

## Integration and Load Testing

Integration and load testing were performed using Docker and the load_test.py script.

The testing process included:

Health endpoint testing
v1 prediction testing
Batch prediction testing
Prometheus metrics testing
Concurrent request testing
Docker container verification

The detailed test results are documented in:

TESTING.md

## Docker

The application is containerized using Docker.

The Docker image installs the required Python dependencies and starts the FastAPI application using Uvicorn.

The application listens on:

0.0.0.0:8000

Docker Compose is used to simplify application startup and configuration.

## Model Volume

The ml/saved_model/ directory is mounted through a named Docker volume.

This allows model files to be managed separately from the application container.

## API Versioning

The project supports two API versions:

/api/v1
/api/v2

API v1 provides the original prediction response.

API v2 provides additional probability information.

Keeping separate API versions allows the API to evolve while maintaining the existing v1 endpoint structure.

## Independent Extension

### GitHub Actions Automated Testing

As an independent extension, GitHub Actions was implemented to automatically run the Pytest test suite whenever code is pushed to the repository or a pull request is created.

The workflow performs the following steps:

- Check out the repository.
- Set up Python 3.14.
- Install the project dependencies.
- Run the Pytest test suite.
- Report the test result.

This provides an automated quality check for future code changes and helps ensure that existing functionality continues to pass the test suite.

The GitHub Actions workflow completed successfully with all tests passing.
## What I Learned

During this project, I learned how to:

Train and save a machine learning model.
Load a trained model inside a FastAPI application.
Create REST API endpoints using FastAPI.
Use Pydantic for request validation.
Create multiple API versions.
Build batch prediction endpoints.
Protect APIs using API keys.
Add request logging and request IDs.
Expose Prometheus metrics.
Write automated API tests using Pytest.
Perform integration and load testing.
Containerize an application using Docker.
Run services using Docker Compose.
Manage project dependencies using requirements.txt.
Use Git and GitHub for version control.
Clean up unused imports and unnecessary dependencies.
Document an ML API project for reproducibility.

## End-to-End Request Flow

A typical prediction request follows this flow:

Client
  ↓
POST /api/v1/predict
  ↓
API Key Verification
  ↓
Pydantic Validation
  ↓
Convert Input to DataFrame
  ↓
Load Trained ML Model
  ↓
Generate Prediction
  ↓
Calculate Confidence
  ↓
Record Prometheus Metric
  ↓
Log Request
  ↓
Return JSON Response

## Reproducibility

The project can be reproduced locally using Docker Compose.

Basic steps:

git clone https://github.com/durai-003/customer-churn-api.git
cd customer-churn-api

Create the .env file and configure the API key.

Then run:

docker compose up --build

After the application starts, open:

http://localhost:8000/docs

The API can then be tested using Swagger UI or the documented curl commands.

## Final Project Checklist
 Machine learning model trained
 Model saved using Joblib
 FastAPI REST API created
 API v1 implemented
 API v2 implemented
 Batch prediction implemented
 Input validation added
 API key security added
 Request logging added
 Prometheus monitoring added
 Automated tests added
 Integration testing completed
 Load testing completed
 Docker support added
 Docker Compose support added
 Project dependencies cleaned
 README documentation completed