import logging
from typing import Dict, Generator
from src.utils.exceptions import LLMPoolError
from src.llm_pool.api_client import APIClient
from src.llm_pool.expert_pool import ExpertPool

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class LLMPool:
    def __init__(self, config: Dict, api_type: str = None):
        logger.debug("Initializing LLMPool")
        self.api_type = api_type or config.get('llm', {}).get('default_api', 'openai')
        self.api_client = APIClient(config.get(self.api_type, {}))
        self.expert_pool = ExpertPool()
        
        self.temperature = config.get('llm', {}).get('temperature', 0.7)
        self.max_tokens = config.get('llm', {}).get('max_tokens', 4096)
        self.context_window = config.get('llm', {}).get('context_window', 128000)
        logger.debug(f"LLMPool initialized with API: {self.api_type}, temperature: {self.temperature}, max_tokens: {self.max_tokens}")
        
        # Note on data usage and retention
        self.data_usage_note = (
            f"Note: Data sent to the {self.api_type.upper()} API will be handled according to the provider's data retention policies. "
            f"Please refer to the {self.api_type.capitalize()} documentation for details on data usage and retention."
        )

    def set_api_type(self, api_type: str):
        if api_type not in ['openai', 'anthropic']:
            raise ValueError(f"Unsupported API type: {api_type}")
        self.api_type = api_type
        self.api_client.set_api_type(api_type)
        logger.debug(f"API type set to: {api_type}")

    def generate_response_stream(self, input_text: str) -> Generator[Dict[str, str], None, None]:
        """
        Generate streaming responses from all experts in the LLM pool.
        
        Args:
            input_text (str): The processed input text.
        
        Yields:
            Dict[str, str]: A dictionary containing the expert name and a chunk of their response.
        
        Raises:
            LLMPoolError: If there's an error generating responses.
        """
        logger.debug(f"Starting generate_response_stream for input: {input_text[:50]}...")
        if not input_text:
            logger.error("Input text is empty")
            raise LLMPoolError("Input text cannot be empty")

        for expert in self.expert_pool.get_all_experts():
            logger.debug(f"Generating response for expert: {expert['name']}")
            prompt = f"{expert['prompt']}\n\nQuestion: {input_text}\n\nResponse:"
            try:
                logger.debug(f"Calling API for expert: {expert['name']}")
                response_chunks = list(self.api_client.generate_response_stream(prompt, self.max_tokens))
                if not response_chunks:
                    logger.warning(f"Empty response for expert: {expert['name']}")
                    yield {
                        "expert": expert["name"],
                        "response": "No response generated"
                    }
                else:
                    for response_chunk in response_chunks:
                        logger.debug(f"Received response chunk for {expert['name']}: {response_chunk}")
                        yield {
                            "expert": expert["name"],
                            "response": response_chunk
                        }
            except LLMPoolError as e:
                logger.error(f"LLMPoolError for {expert['name']}: {str(e)}")
                yield {
                    "expert": expert["name"],
                    "response": f"Error: {str(e)}"
                }
            except Exception as e:
                logger.error(f"Unexpected error for {expert['name']}: {str(e)}")
                yield {
                    "expert": expert["name"],
                    "response": f"Unexpected error: {str(e)}"
                }
        
        logger.debug("Generating data usage note")
        yield {
            "expert": "System",
            "response": self.data_usage_note
        }
        logger.debug("Finished generate_response_stream")

    @property
    def experts(self):
        return self.expert_pool.get_all_experts()

    def get_expert_names(self):
        return self.expert_pool.get_expert_names()

    def get_expert_prompt(self, expert_name: str) -> str:
        return self.expert_pool.get_expert_prompt(expert_name)

    def add_expert(self, name: str, prompt: str) -> None:
        self.expert_pool.add_expert(name, prompt)

    def remove_expert(self, name: str) -> None:
        self.expert_pool.remove_expert(name)

    def update_expert(self, name: str, new_prompt: str) -> None:
        self.expert_pool.update_expert(name, new_prompt)

    def get_all_experts(self):
        return self.expert_pool.get_all_experts()

    def set_api_type(self, api_type: str) -> None:
        self.api_client.set_api_type(api_type)
