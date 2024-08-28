import logging
import sys
import os
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask, render_template, request, jsonify
from src.web import create_app
from src.config.config_loader import load_config
from src.llm_pool.llm_pool import LLMPool
from src.moderator.moderator import Moderator
from src.heuristics.principles import Principles
from src.ab_testing import ABTestRunner

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
config = load_config()

# Create Flask app
app = create_app(config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/discuss', methods=['POST'])
def discuss():
    data = request.json
    api_type = data.get('api_type', 'openai')
    input_text = data.get('input_text', '')

    llm_pool = LLMPool(config, api_type=api_type)
    principles = Principles(config['principles']['version_control_file'])
    moderator = Moderator(llm_pool, principles)

    responses = list(moderator.start_discussion_stream(input_text))
    return jsonify(responses)

@app.route('/api/ab_test', methods=['POST'])
def ab_test():
    data = request.json
    input_text = data.get('input_text', '')

    ab_runner = ABTestRunner(config)
    results = ab_runner.run_ab_test(input_text)
    analysis = ab_runner.analyze_results(results)
    return jsonify(analysis)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define service URLs
REASONING_ENGINE_URL = os.getenv("REASONING_ENGINE_URL", "http://reasoning_engine:5002")

@app.get("/")
async def root():
    return {"message": "Welcome to the Collaborative AI Reasoning System API Gateway"}

@app.post("/reason")
async def reason(data: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{REASONING_ENGINE_URL}/reason", json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while requesting the reasoning engine: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
