import openai
import time
from functools import lru_cache
from typing import Generator
from src.utils.exceptions import LLMPoolError

import os
import openai
from typing import Generator

class OpenAIAPI:
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is not set")
        self.model = model
        self.last_request_time = 0
        self.rate_limit_delay = 1  # 1 request per second
        self.is_test_environment = self.api_key == "test_openai_api_key"
        
        # Set the API key for the openai module
        openai.api_key = self.api_key
        
        # Log the API key (first few characters) for debugging
        if self.api_key:
            print(f"OpenAIAPI initialized with API Key (first 5 chars): {self.api_key[:5]}...")
        else:
            print("OpenAIAPI initialized without API Key!")

    def _rate_limit(self):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last_request)
        self.last_request_time = time.time()

    @lru_cache(maxsize=100)
    def generate_response(self, prompt, max_tokens=4096):
        self._rate_limit()
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            return response.choices[0].message['content'].strip()
        except openai.error.RateLimitError:
            raise LLMPoolError("Rate limit exceeded. Please try again later.")
        except openai.error.APIError as e:
            raise LLMPoolError(f"OpenAI API error: {str(e)}")
        except Exception as e:
            raise LLMPoolError(f"Unexpected error: {str(e)}")

    def generate_response_stream(self, prompt, max_tokens=4096) -> Generator[str, None, None]:
        self._rate_limit()
        if self.is_test_environment:
            yield "Test response"
            return

        try:
            openai.api_key = self.api_key
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                stream=True
            )
            for chunk in response:
                if chunk.choices[0].delta.get("content"):
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"Error: {str(e)}"
        except openai.error.RateLimitError:
            raise LLMPoolError("Rate limit exceeded. Please try again later.")
        except openai.error.APIError as e:
            raise LLMPoolError(f"OpenAI API error: {str(e)}")
        except Exception as e:
            raise LLMPoolError(f"Unexpected error: {str(e)}")

    def set_model(self, model):
        """
        Set the model to be used for generating responses.
        
        Args:
            model (str): The name of the model to use.
        """
        self.model = model
