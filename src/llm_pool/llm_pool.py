import openai
from typing import Dict, List
from src.utils.exceptions import LLMPoolError

class LLMPool:
    def __init__(self, config: Dict):
        self.model = config['model']
        self.temperature = config['temperature']
        self.max_tokens = config['max_tokens']
        self.experts = [
            {"name": "Analyst", "prompt": "You are an analytical expert. Provide a logical and data-driven perspective."},
            {"name": "Creative", "prompt": "You are a creative expert. Think outside the box and provide innovative ideas."},
            {"name": "Critic", "prompt": "You are a critical thinker. Identify potential flaws and provide constructive criticism."},
            {"name": "Synthesizer", "prompt": "You are a synthesizer. Combine different ideas and perspectives into a cohesive whole."},
            {"name": "Ethicist", "prompt": "You are an ethics expert. Consider the moral and ethical implications of ideas and decisions."}
        ]

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

    def generate_response(self, input_text: str) -> List[Dict]:
        """
        Generate responses from all experts in the LLM pool.
        
        Args:
            input_text (str): The processed input text.
        
        Returns:
            List[Dict]: A list of responses from each expert.
        
        Raises:
            LLMPoolError: If there's an error generating responses.
        """
        if not input_text:
            raise LLMPoolError("Input text cannot be empty")

        responses = []
        for expert in self.experts:
            prompt = f"{expert['prompt']}\n\nQuestion: {input_text}\n\nResponse:"
            try:
                response = openai.Completion.create(
                    engine=self.model,
                    prompt=prompt,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    n=1,
                    stop=None
                )
                responses.append({
                    "expert": expert["name"],
                    "response": response.choices[0].text.strip()
                })
            except Exception as e:
                responses.append({
                    "expert": expert["name"],
                    "response": f"Error generating response: {str(e)}"
                })
        return responses

    def get_expert_names(self) -> List[str]:
        return [expert["name"] for expert in self.experts]

    def get_expert_prompt(self, expert_name: str) -> str:
        for expert in self.experts:
            if expert["name"] == expert_name:
                return expert["prompt"]
        raise ValueError(f"Expert '{expert_name}' not found")
