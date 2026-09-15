from prometheus_client import Counter

churn_predictions_total = Counter(
    "churn_predictions_total",
    "Total number of successful churn predictions",
    ["prediction"]
)