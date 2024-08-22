import openai
from typing import Dict, List

class LLMPool:
    def __init__(self, config: Dict):
        self.model = config['model']
        self.temperature = config['temperature']
        self.max_tokens = config['max_tokens']
        self.experts = [
            {"name": "Analyst", "prompt": "You are an analytical expert. Provide a logical and data-driven perspective."},
            {"name": "Creative", "prompt": "You are a creative expert. Think outside the box and provide innovative ideas."},
            {"name": "Critic", "prompt": "You are a critical thinker. Identify potential flaws and provide constructive criticism."}
        ]

    def generate_response(self, input_text: str) -> List[Dict]:
        # Existing implementation...

    def get_expert_names(self) -> List[str]:
        return [expert["name"] for expert in self.experts]

    def get_expert_prompt(self, expert_name: str) -> str:
        for expert in self.experts:
            if expert["name"] == expert_name:
                return expert["prompt"]
        raise ValueError(f"Expert '{expert_name}' not found")
        """
        Generate responses from all experts in the LLM pool.
        
        Args:
            input_text (str): The processed input text.
        
        Returns:
            List[Dict]: A list of responses from each expert.
        """
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
