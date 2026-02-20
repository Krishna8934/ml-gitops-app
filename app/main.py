import logging
import time
from fastapi import FastAPI, Request
from fastapi.responses import Response, HTMLResponse
from fastapi.templating import Jinja2Templates
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

templates = Jinja2Templates(directory="app/templates")

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

@app.get("/" , response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})


@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/about")
def about():
    return {
        "developer":"Krishna",
        "project":"DevOps GitOps Automation  Project",
        "linkedin" : "https://www.linkedin.com/in/krishna-mishra-cse?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app"
    }


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