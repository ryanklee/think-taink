from typing import Dict, Any
from .agent import Agent
import anthropic

class ClaudeAgent(Agent):
    """
    Claude-based agent implementation.
    """

    def __init__(self, agent_id: str, config: Dict[str, Any]):
        super().__init__(agent_id, config)
        self.api_key = config.get('api_key')
        self.model = config.get('model', 'claude-instant-1')
        self.client = anthropic.Client(api_key=self.api_key)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = input_data.get('prompt', '')
        try:
            response = self.client.completion(
                model=self.model,
                prompt=f"\n\nHuman: {prompt}\n\nAssistant:",
                max_tokens_to_sample=300,
            )
            return {
                'output': response.completion,
                'status': 'success'
            }
        except Exception as e:
            return {
                'output': str(e),
                'status': 'error'
            }

    def update_knowledge(self, new_knowledge: Dict[str, Any]) -> None:
        # For this simple implementation, we'll just update the config
        self.config.update(new_knowledge)

    def get_state(self) -> Dict[str, Any]:
        return {
            'agent_id': self.agent_id,
            'config': self.config,
            'model': self.model
        }

    def set_state(self, state: Dict[str, Any]) -> None:
        self.agent_id = state.get('agent_id', self.agent_id)
        self.config = state.get('config', self.config)
        self.model = state.get('model', self.model)
        self.client = anthropic.Client(api_key=self.config.get('api_key', self.api_key))
