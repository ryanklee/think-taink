import logging
from typing import Generator
from src.utils.exceptions import LLMPoolError
from src.llm_pool.anthropic_api import AnthropicAPI
from src.llm_pool.openai_api import OpenAIAPI

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, config: dict):
        self.api_type = config.get('api_type', 'anthropic')
        self.model = config.get('model')
        
        if self.api_type == 'anthropic':
            self.api_key = config.get('anthropic', {}).get('api_key') or os.environ.get('ANTHROPIC_API_KEY')
            if not self.api_key:
                logger.warning("Anthropic API key is missing in the configuration and environment. Using a default key for testing.")
                self.api_key = "default_anthropic_api_key_for_testing"
            self.api = AnthropicAPI(self.api_key, model=self.model)
        elif self.api_type == 'openai':
            self.api_key = config.get('openai', {}).get('api_key')
            if not self.api_key:
                logger.error("OpenAI API key is missing in the configuration")
                raise ValueError("OpenAI API key is missing in the configuration")
            self.api = OpenAIAPI(self.api_key, model=self.model)
        else:
            raise ValueError(f"Unsupported API type: {self.api_type}")
        
        logger.debug(f"APIClient initialized with API: {self.api_type}, model: {self.model}")
        logger.debug(f"API Key (first 5 chars): {self.api_key[:5]}...")
        
        # Set a flag for test environment
        self.is_test_environment = self.api_key.startswith('test_')

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
