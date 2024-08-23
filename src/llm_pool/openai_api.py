import openai
import time
from functools import lru_cache
from src.utils.exceptions import LLMPoolError

class OpenAIAPI:
    def __init__(self, api_key, model="gpt-4o-mini"):
        openai.api_key = api_key
        self.model = model
        self.last_request_time = 0
        self.rate_limit_delay = 1  # 1 request per second

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

    def set_model(self, model):
        """
        Set the model to be used for generating responses.
        
        Args:
            model (str): The name of the model to use.
        """
        self.model = model
