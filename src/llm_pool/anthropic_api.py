import anthropic
import os
from typing import Generator
from src.utils.exceptions import LLMPoolError

class AnthropicAPI:
    def __init__(self, api_key=None, model="claude-3-5-sonnet-20240620"):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key is missing")
        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def generate_response(self, prompt, max_tokens=1000, temperature=0):
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            raise LLMPoolError(f"Anthropic API error: {str(e)}")

    def generate_response_stream(self, prompt, max_tokens=1000, temperature=0) -> Generator[str, None, None]:
        try:
            with self.client.messages.stream(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            ) as stream:
                for text in stream.text_stream:
                    yield text
        except Exception as e:
            raise LLMPoolError(f"Anthropic API error: {str(e)}")

    def set_model(self, model):
        self.model = model
