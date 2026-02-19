import logging
import time
from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, generate_latest
from .schemas import InputData
from .model import predict_logic

# ---------------- Logging Configuration ----------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# ---------------- FastAPI App ----------------

app = FastAPI(title="ML GitOps App")

# ---------------- Prometheus Metrics ----------------

REQUEST_COUNT = Counter(
    "ml_app_requests_total",
    "Total number of API requests",
    ["method", "endpoint"],
)

REQUEST_LATENCY = Histogram(
    "ml_app_request_latency_seconds",
    "Latency of API requests",
    ["endpoint"],
)

# ---------------- Routes ----------------

@app.get("/")
def home():
    return {"message": "ML GitOps App Running - Version 2 🚀"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(data: InputData):
    logger.info(f"Received prediction request with value: {data.value}")

    # Increment request counter
    REQUEST_COUNT.labels(method="POST", endpoint="/predict").inc()

    start_time = time.time()

    prediction = predict_logic(data.value)

    # Record latency
    REQUEST_LATENCY.labels(endpoint="/predict").observe(
        time.time() - start_time
    )

    logger.info(f"Prediction result: {prediction}")

    return {
        "input": data.value,
        "prediction": prediction
    }


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
