from typing import List, Dict
from src.heuristics.principles import Principles
from src.llm_pool.llm_pool import LLMPool

class Reflector:
    def __init__(self, principles: Principles, llm_pool: LLMPool):
        self.principles = principles
        self.llm_pool = llm_pool

    def reflect_on_principles(self, discussion_history: List[Dict]) -> Dict[str, str]:
        reflection_prompt = self._generate_reflection_prompt(discussion_history)
        reflection_response = self.llm_pool.generate_response(reflection_prompt)
        return self._parse_reflection_response(reflection_response)

    def _generate_reflection_prompt(self, discussion_history: List[Dict]) -> str:
        prompt = "Analyze the following discussion and suggest improvements to our guiding principles:\n\n"
        for entry in discussion_history:
            prompt += f"{entry['expert']}: {entry['response']}\n"
        prompt += "\nCurrent principles:\n"
        for name, description in self.principles.get_principles().items():
            prompt += f"- {name}: {description}\n"
        prompt += "\nSuggest improvements, additions, or removals to these principles based on the discussion."
        return prompt

    def _parse_reflection_response(self, response: str) -> Dict[str, str]:
        # TODO: Implement a more sophisticated parsing method
        # For now, we'll assume the response is a simple list of suggestions
        suggestions = {}
        for line in response.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                suggestions[key.strip()] = value.strip()
        return suggestions
