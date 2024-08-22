import logging
from fastapi import FastAPI
from input_processing.processor import InputProcessor
from llm_pool.llm_pool import LLMPool
from config.config_loader import load_config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
config = load_config()

# Initialize FastAPI app
app = FastAPI()

# Initialize components
input_processor = InputProcessor()
llm_pool = LLMPool(config['llm'])

@app.post("/process")
async def process_input(input_text: str):
    try:
        processed_input = input_processor.process(input_text)
        response = llm_pool.generate_response(processed_input)
        return {"result": response}
    except Exception as e:
        logger.error(f"Error processing input: {str(e)}")
        return {"error": "An error occurred while processing the input"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
