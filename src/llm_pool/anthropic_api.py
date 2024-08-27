import anthropic
from typing import Generator
from src.utils.exceptions import LLMPoolError

class AnthropicAPI:
    def __init__(self, api_key, model="claude-3-sonnet-20240229"):
        self.api_key = api_key
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.is_test_environment = api_key == "test_api_key"

    def generate_response_stream(self, prompt, max_tokens=4096) -> Generator[str, None, None]:
        if self.is_test_environment:
            yield "Test response"
            return

        try:
            with self.client.messages.stream(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
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

    def set_model(self, model):
        self.model = model

    def generate_response(self, prompt, max_tokens=4096) -> str:
        if self.is_test_environment:
            return "Test response"

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content
        except anthropic.APIError as e:
            raise LLMPoolError(f"Anthropic API error: {str(e)}")
        except Exception as e:
            raise LLMPoolError(f"Unexpected error: {str(e)}")
