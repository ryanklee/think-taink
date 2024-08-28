import anthropic
import time
from typing import Generator, Dict, List
from src.utils.exceptions import LLMPoolError

import os
import anthropic
from typing import Generator

class AnthropicAPI:
    def __init__(self, api_key=None, model="claude-3-sonnet-20240229"):
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("Anthropic API key is not set")
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model
        self.api = self.client  # Add this line to maintain compatibility
        self.is_test_environment = self.api_key == "test_anthropic_api_key"
        self.last_request_time = 0
        self.daily_request_count = 0
        self.rate_limit_delay = 0.1  # 10 requests per second

    def _rate_limit(self):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last_request)
        self.last_request_time = time.time()
        self.daily_request_count += 1
        if self.daily_request_count > 1000:
            raise LLMPoolError("Daily request limit exceeded")

    def generate_response_stream(self, prompt, max_tokens=4096, system_prompt=None) -> Generator[str, None, None]:
        if self.is_test_environment:
            yield "Test response"
            return

        self._rate_limit()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            with self.client.messages.stream(
                model=self.model,
                max_tokens=max_tokens,
                messages=messages
            ) as stream:
                for text in stream.text_stream:
                    yield text
        except anthropic.APIError as e:
            raise LLMPoolError(f"Anthropic API error: {str(e)}")
        except anthropic.APIConnectionError as e:
            raise LLMPoolError(f"Anthropic API connection error: {str(e)}")
        except anthropic.RateLimitError as e:
            raise LLMPoolError(f"Anthropic API rate limit exceeded: {str(e)}")
        except Exception as e:
            raise LLMPoolError(f"Unexpected error in Anthropic API: {str(e)}")

    def generate_chat_response(self, messages: List[Dict[str, str]], max_tokens=4096, system_prompt=None) -> str:
        if self.is_test_environment:
            return "Test chat response"

        self._rate_limit()

        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=messages
            )
            return response.content
        except anthropic.APIError as e:
            raise LLMPoolError(f"Anthropic API error: {str(e)}")
        except Exception as e:
            raise LLMPoolError(f"Unexpected error: {str(e)}")

    def analyze_document(self, document: str, file_type: str, analysis_type: str, system_prompt=None) -> Dict:
        if self.is_test_environment:
            return {"analysis": "Test document analysis"}

        self._rate_limit()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": f"Analyze this {file_type} document. Perform a {analysis_type} analysis:\n\n{document}"})

        try:
            response = self.client.messages.create(
                model=self.model,
                messages=messages
            )
            return {"analysis": response.content}
        except anthropic.APIError as e:
            raise LLMPoolError(f"Anthropic API error: {str(e)}")
        except Exception as e:
            raise LLMPoolError(f"Unexpected error: {str(e)}")

    def set_model(self, model):
        self.model = model
