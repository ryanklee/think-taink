from typing import List, Dict
from src.llm_pool.llm_pool import LLMPool

class PoolEvolution:
    def __init__(self, llm_pool: LLMPool):
        self.llm_pool = llm_pool

    def evolve_pool(self, discussion_history: List[Dict]) -> None:
        """
        Evolve the expert pool based on the discussion history.
        This method should analyze the discussion and suggest changes to the expert pool.
        """
        evolution_prompt = self._generate_evolution_prompt(discussion_history)
        evolution_response = self.llm_pool.generate_response(evolution_prompt)
        suggestions = self._parse_evolution_response(evolution_response)
        self._apply_pool_changes(suggestions)

    def _generate_evolution_prompt(self, discussion_history: List[Dict]) -> str:
        prompt = "Analyze the following discussion and suggest improvements to our expert pool:\n\n"
        for entry in discussion_history:
            prompt += f"{entry['expert']}: {entry['response']}\n"
        prompt += "\nCurrent experts:\n"
        for expert in self.llm_pool.experts:
            prompt += f"- {expert['name']}: {expert['prompt']}\n"
        prompt += "\nSuggest additions, removals, or modifications to the expert pool based on the discussion."
        return prompt

    def _parse_evolution_response(self, response: str) -> Dict[str, Dict]:
        suggestions = {}
        current_expert = None
        for line in response.split('\n'):
            if line.startswith('Add:') or line.startswith('Modify:') or line.startswith('Remove:'):
                action, expert_name = line.split(':')
                current_expert = expert_name.strip()
                suggestions[current_expert] = {"action": action.strip().lower(), "prompt": ""}
            elif current_expert and ':' in line:
                suggestions[current_expert]["prompt"] = line.split(':', 1)[1].strip()
        return suggestions

    def _apply_pool_changes(self, suggestions: Dict[str, Dict]) -> None:
        for expert_name, change in suggestions.items():
            if change["action"] == "add":
                self.llm_pool.add_expert(expert_name, change["prompt"])
            elif change["action"] == "modify":
                self.llm_pool.update_expert(expert_name, change["prompt"])
            elif change["action"] == "remove":
                self.llm_pool.remove_expert(expert_name)
