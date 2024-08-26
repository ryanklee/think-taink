import anthropic
from typing import Generator
from src.utils.exceptions import LLMPoolError

class AnthropicAPI:
    def __init__(self, api_key, model="claude-3-sonnet-20240229"):
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
        except Exception as e:
            raise LLMPoolError(f"Unexpected error: {str(e)}")

    def set_model(self, model):
        self.model = model