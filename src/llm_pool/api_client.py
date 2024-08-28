import logging
import os
from typing import Generator, List, Dict
from src.utils.exceptions import LLMPoolError
from src.llm_pool.anthropic_api import AnthropicAPI

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, config: dict):
        self.api_type = 'anthropic'
        self.model = config.get('model')
        
        self.api_key = config.get('anthropic', {}).get('api_key') or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            logger.warning("Anthropic API key is missing in the configuration and environment. Using a default key for testing.")
            self.api_key = "default_anthropic_api_key_for_testing"
        self.api = AnthropicAPI(self.api_key, model=self.model)
        
        logger.debug(f"APIClient initialized with API: {self.api_type}, model: {self.model}")
        logger.debug(f"API Key (first 5 chars): {self.api_key[:5]}...")
        
        # Set a flag for test environment
        self.is_test_environment = self.api_key.startswith('test_')

    def generate_response_stream(self, prompt: str, max_tokens: int, system_prompt: str = None) -> Generator[str, None, None]:
        try:
            return self.api.generate_response_stream(prompt, max_tokens, system_prompt=system_prompt)
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise LLMPoolError(f"Error generating response: {str(e)}")

    def generate_chat_response(self, messages: List[Dict[str, str]], max_tokens: int, system_prompt: str = None) -> str:
        try:
            return self.api.generate_chat_response(messages, max_tokens, system_prompt=system_prompt)
        except Exception as e:
            logger.error(f"Error generating chat response: {str(e)}")
            raise LLMPoolError(f"Error generating chat response: {str(e)}")

    def analyze_document(self, document: str, file_type: str, analysis_type: str, system_prompt: str = None) -> Dict:
        try:
            return self.api.analyze_document(document, file_type, analysis_type, system_prompt=system_prompt)
        except Exception as e:
            logger.error(f"Error analyzing document: {str(e)}")
            raise LLMPoolError(f"Error analyzing document: {str(e)}")

    def set_model(self, model: str) -> None:
        self.model = model
        self.api.set_model(model)

    def set_api_type(self, api_type: str) -> None:
        if api_type != 'anthropic':
            raise ValueError(f"Unsupported API type: {api_type}")
        self.api_type = api_type
