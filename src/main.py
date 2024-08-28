import logging
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from src.config.config_loader import load_config
from src.llm_pool.llm_pool import LLMPool
from src.moderator.moderator import Moderator
from src.heuristics.principles import Principles
from src.ab_testing import ABTestRunner

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    # Load configuration
    config = load_config()

    app = FastAPI()

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    @app.get("/")
    async def root():
        return {"message": "Welcome to the Collaborative AI Reasoning System"}

    @app.post("/api/discuss")
    async def discuss(data: dict):
        api_type = data.get('api_type', 'openai')
        input_text = data.get('input_text', '')

        llm_pool = LLMPool(config, api_type=api_type)
        principles = Principles(config['principles']['version_control_file'])
        moderator = Moderator(llm_pool, principles)

        responses = list(moderator.start_discussion_stream(input_text))
        return responses

    @app.post("/api/ab_test")
    async def ab_test(data: dict):
        input_text = data.get('input_text', '')

        ab_runner = ABTestRunner(config)
        results = ab_runner.run_ab_test(input_text)
        analysis = ab_runner.analyze_results(results)
        return analysis

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
