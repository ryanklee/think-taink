import logging
from typing import Generator
from src.utils.exceptions import LLMPoolError
from src.llm_pool.anthropic_api import AnthropicAPI
from src.llm_pool.openai_api import OpenAIAPI

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, config: dict):
        self.api_type = config.get('api_type', 'anthropic')
        self.api_key = config.get('api_key')
        self.model = config.get('model')
        
        if not self.api_key:
            logger.error("API key is missing in the configuration")
            raise ValueError("API key is missing in the configuration")
        
        if self.api_type == 'anthropic':
            self.api = AnthropicAPI(self.api_key, model=self.model)
        elif self.api_type == 'openai':
            self.api = OpenAIAPI(self.api_key, model=self.model)
        else:
            raise ValueError(f"Unsupported API type: {self.api_type}")
        
        logger.debug(f"APIClient initialized with API: {self.api_type}, model: {self.model}")
        logger.debug(f"API Key (first 5 chars): {self.api_key[:5]}...")

    def generate_response_stream(self, prompt: str, max_tokens: int) -> Generator[str, None, None]:
        try:
            return self.api.generate_response_stream(prompt, max_tokens)
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise LLMPoolError(f"Error generating response: {str(e)}")

    def set_model(self, model: str) -> None:
        self.model = model
        self.api.set_model(model)

    def set_api_type(self, api_type: str) -> None:
        if api_type not in ['anthropic', 'openai']:
            raise ValueError(f"Unsupported API type: {api_type}")
        self.api_type = api_type
        if self.api_type == 'anthropic':
            self.api = AnthropicAPI(self.api_key, model=self.model)
        else:
            self.api = OpenAIAPI(self.api_key, model=self.model)
