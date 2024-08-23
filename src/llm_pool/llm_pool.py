from typing import Dict, List, Generator
from src.utils.exceptions import LLMPoolError
from src.llm_pool.openai_api import OpenAIAPI

class LLMPool:
    def __init__(self, config: Dict):
        self.api = OpenAIAPI(config.get('openai', {}).get('api_key', ''), model=config.get('model', 'gpt-4o-mini'))
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 4096)  # Updated to match gpt-4o-mini's max output tokens
        self.context_window = 128000  # Context window for gpt-4o-mini
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
        if not input_text:
            raise LLMPoolError("Input text cannot be empty")

        for expert in self.experts:
            prompt = f"{expert['prompt']}\n\nQuestion: {input_text}\n\nResponse:"
            try:
                for response_chunk in self.api.generate_response_stream(
                    prompt, 
                    max_tokens=4096 if self.api.model == 'gpt-4o' else self.max_tokens
                ):
                    yield {
                        "expert": expert["name"],
                        "response": response_chunk
                    }
            except Exception as e:
                yield {
                    "expert": expert["name"],
                    "response": f"Error generating response: {str(e)}"
                }
        
        # Yield the data usage note
        yield {
            "expert": "System",
            "response": self.data_usage_note
        }

    def get_expert_names(self) -> List[str]:
        return [expert["name"] for expert in self.experts]

    def get_expert_prompt(self, expert_name: str) -> str:
        for expert in self.experts:
            if expert["name"] == expert_name:
                return expert["prompt"]
        raise ValueError(f"Expert '{expert_name}' not found")
