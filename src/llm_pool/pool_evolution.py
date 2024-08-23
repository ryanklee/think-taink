from typing import List, Dict
import logging
from src.llm_pool.llm_pool import LLMPool
from src.utils.exceptions import PoolEvolutionError

class PoolEvolution:
    def __init__(self, llm_pool: LLMPool):
        self.llm_pool = llm_pool

    def evolve_pool(self, discussion_history: List[Dict]) -> None:
        """
        Evolve the expert pool based on the discussion history.
        This method should analyze the discussion and suggest changes to the expert pool.
        """
        try:
            evolution_prompt = self._generate_evolution_prompt(discussion_history)
            evolution_response = self.llm_pool.generate_response(evolution_prompt)
            suggestions = self._parse_evolution_response(evolution_response)
            self._apply_pool_changes(suggestions)
        except Exception as e:
            logging.error(f"Error during pool evolution: {str(e)}")
            raise PoolEvolutionError(f"Failed to evolve expert pool: {str(e)}")

    def _generate_evolution_prompt(self, discussion_history: List[Dict]) -> str:
        prompt = "Analyze the following discussion and suggest improvements to our expert pool:\n\n"
        for entry in discussion_history:
            prompt += f"{entry['expert']}: {entry['response']}\n"
        prompt += "\nCurrent experts:\n"
        for expert_name in self.llm_pool.get_expert_names():
            prompt += f"- {expert_name}: {self.llm_pool.get_expert_prompt(expert_name)}\n"
        prompt += "\nSuggest additions, removals, or modifications to the expert pool based on the discussion."
        return prompt

    def _parse_evolution_response(self, response: str) -> Dict[str, Dict]:
        suggestions = {}
        for line in response.split('\n'):
            parts = line.split(':', 2)
            if len(parts) == 3:
                action, expert_name, prompt = parts
                action = action.strip().lower()
                expert_name = expert_name.strip()
                prompt = prompt.strip()
                suggestions[expert_name] = {"action": action, "prompt": prompt}
        return suggestions

    def _apply_pool_changes(self, suggestions: Dict[str, Dict]) -> None:
        for expert_name, change in suggestions.items():
            action = change["action"].lower()
            if action == "add":
                self.llm_pool.add_expert(expert_name, change["prompt"])
            elif action == "modify":
                self.llm_pool.update_expert(expert_name, change["prompt"])
            elif action == "remove":
                self.llm_pool.remove_expert(expert_name)
