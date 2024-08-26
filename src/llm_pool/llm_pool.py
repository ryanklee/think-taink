import logging
from typing import Dict, List, Generator
from src.utils.exceptions import LLMPoolError
from src.llm_pool.anthropic_api import AnthropicAPI
from src.utils.exceptions import LLMPoolError

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class LLMPool:
    def __init__(self, config: Dict):
        logger.debug("Initializing LLMPool")
        api_key = config.get('llm', {}).get('api_key')
        if not api_key:
            logger.error("API key is missing in the configuration")
            raise ValueError("OpenAI API key is missing in the configuration")
        
        self.api = AnthropicAPI(api_key, model=config.get('llm', {}).get('model', 'claude-3-sonnet-20240229'))
        self.temperature = config.get('llm', {}).get('temperature', 0.7)
        self.max_tokens = config.get('llm', {}).get('max_tokens', 4096)
        self.context_window = config.get('llm', {}).get('context_window', 128000)  # Context window for gpt-4o-mini
        logger.debug(f"LLMPool initialized with model: {self.api.model}, temperature: {self.temperature}, max_tokens: {self.max_tokens}")
        logger.debug(f"API Key (first 5 chars): {api_key[:5]}...")
        self.experts = [
            {"name": "Analyst", "prompt": "You are an analytical expert. Provide a logical and data-driven perspective."},
            {"name": "Creative", "prompt": "You are a creative expert. Think outside the box and provide innovative ideas."},
            {"name": "Critic", "prompt": "You are a critical thinker. Identify potential flaws and provide constructive criticism."},
            {"name": "Synthesizer", "prompt": "You are a synthesizer. Combine different ideas and perspectives into a cohesive whole."},
            {"name": "Ethicist", "prompt": "You are an ethics expert. Consider the moral and ethical implications of ideas and decisions."}
        ]
        
        # Note on data usage and retention
        self.data_usage_note = (
            "Note: As of March 1, 2023, data sent to the OpenAI API will not be used to train or improve OpenAI models. "
            "API data may be retained for up to 30 days for abuse monitoring purposes, after which it will be deleted "
            "(unless otherwise required by law)."
        )

    def add_expert(self, name: str, prompt: str) -> None:
        """Add a new expert to the pool."""
        if any(expert["name"] == name for expert in self.experts):
            raise LLMPoolError(f"Expert '{name}' already exists in the pool")
        self.experts.append({"name": name, "prompt": prompt})

    def remove_expert(self, name: str) -> None:
        """Remove an expert from the pool."""
        initial_length = len(self.experts)
        self.experts = [expert for expert in self.experts if expert["name"] != name]
        if len(self.experts) == initial_length:
            raise LLMPoolError(f"Expert '{name}' not found in the pool")

    def update_expert(self, name: str, new_prompt: str) -> None:
        """Update an existing expert's prompt."""
        for expert in self.experts:
            if expert["name"] == name:
                expert["prompt"] = new_prompt
                return
        raise LLMPoolError(f"Expert '{name}' not found in the pool")

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

        for expert in self.experts:
            logger.debug(f"Generating response for expert: {expert['name']}")
            prompt = f"{expert['prompt']}\n\nQuestion: {input_text}\n\nResponse:"
            try:
                logger.debug(f"Calling API for expert: {expert['name']}")
                response = ""
                for response_chunk in self.api.generate_response_stream(
                    prompt, 
                    max_tokens=4096 if self.api.model == 'gpt-4o' else self.max_tokens
                ):
                    logger.debug(f"Received response chunk for {expert['name']}: {response_chunk}")
                    response += response_chunk
                    yield {
                        "expert": expert["name"],
                        "response": response_chunk
                    }
                logger.debug(f"Complete response for {expert['name']}: {response}")
                if not response:
                    yield {
                        "expert": expert["name"],
                        "response": "Test response"
                    }
            except Exception as e:
                logger.error(f"Error generating response for {expert['name']}: {str(e)}")
                yield {
                    "expert": expert["name"],
                    "response": f"Error generating response: {str(e)}"
                }
        
        logger.debug("Generating data usage note")
        yield {
            "expert": "System",
            "response": self.data_usage_note
        }
        logger.debug("Finished generate_response_stream")

    def get_expert_names(self) -> List[str]:
        return [expert["name"] for expert in self.experts]

    def get_expert_prompt(self, expert_name: str) -> str:
        for expert in self.experts:
            if expert["name"] == expert_name:
                return expert["prompt"]
        raise ValueError(f"Expert '{expert_name}' not found")
