import logging
from fastapi import FastAPI
from fastapi.responses import Response
import time
from prometheus_client import Counter, Histogram, generate_latest
from .schemas import InputData
from .model import predict_logic

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


app = FastAPI(title="ML GitOps App")

REQUEST_COUNT = Counter("request_count", "Total API Requests")
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency")

@app.get("/")
def home():
   return {"message": "ML GitOps App Running - Version 2 🚀"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/predict")
def predict(data: InputData):
    logger.info(f"Received prediction request with value: {data.value}")

    REQUEST_COUNT.inc()
    start_time = time.time()

    prediction = predict_logic(data.value)

    REQUEST_LATENCY.observe(time.time() - start_time)

    logger.info(f"Prediction result: {prediction}")

    return {
        "input": data.value,
        "prediction": prediction
    }


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
