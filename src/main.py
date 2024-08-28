import logging
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app, Counter, Histogram
from src.config.config_loader import load_config
from src.llm_pool.llm_pool import LLMPool
from src.moderator.moderator import Moderator
from src.heuristics.principles import Principles

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up Prometheus metrics
REQUESTS = Counter('app_requests_total', 'Total app HTTP requests')
RESPONSES = Counter('app_responses_total', 'Total app HTTP responses', ['status_code'])
LATENCY = Histogram('app_request_latency_seconds', 'Request latency in seconds')

def create_app():
    # Load configuration
    config = load_config()

    app = FastAPI()

    # Add Prometheus metrics
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        REQUESTS.inc()
        with LATENCY.time():
            response = await call_next(request)
        RESPONSES.labels(status_code=response.status_code).inc()
        return response

    @app.get("/")
    async def root():
        return {"message": "Welcome to the Collaborative AI Reasoning System"}

    @app.post("/api/discuss")
    async def discuss(data: dict):
        input_text = data.get('input_text', '')

        llm_pool = LLMPool(config)
        principles = Principles(config['principles']['version_control_file'])
        moderator = Moderator(llm_pool, principles)

        responses = list(moderator.start_discussion_stream(input_text))
        return responses

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
