from typing import List, Dict
import logging
from src.heuristics.principles import Principles
from src.llm_pool.llm_pool import LLMPool

class Reflector:
    def __init__(self, principles: Principles, llm_pool: LLMPool):
        self.principles = principles
        self.llm_pool = llm_pool

    def reflect_on_principles(self, discussion_history: List[Dict]) -> Dict[str, str]:
        """
        Reflect on the principles based on the discussion history and suggest improvements.

        Args:
            discussion_history (List[Dict]): A list of dictionaries containing the discussion entries.

        Returns:
            Dict[str, str]: A dictionary of suggested improvements to the principles.

        Raises:
            ValueError: If the reflection response cannot be parsed.
        """
        try:
            reflection_prompt = self._generate_reflection_prompt(discussion_history)
            reflection_response = self.llm_pool.generate_response(reflection_prompt)
            suggestions = self._parse_reflection_response(reflection_response)
            self.principles.apply_reflector_suggestions(suggestions)
            return suggestions
        except Exception as e:
            logging.error(f"Error in reflect_on_principles: {str(e)}")
            raise

    def _generate_reflection_prompt(self, discussion_history: List[Dict]) -> str:
        """
        Generate a prompt for reflection based on the discussion history and current principles.

        Args:
            discussion_history (List[Dict]): A list of dictionaries containing the discussion entries.

        Returns:
            str: The generated reflection prompt.
        """
        prompt = "Analyze the following discussion and suggest improvements to our guiding principles:\n\n"
        for entry in discussion_history:
            prompt += f"{entry['expert']}: {entry['response']}\n"
        prompt += "\nCurrent principles:\n"
        for name, description in self.principles.get_principles().items():
            prompt += f"- {name}: {description}\n"
        prompt += "\nSuggest improvements, additions, or removals to these principles based on the discussion."
        return prompt

    def _parse_reflection_response(self, response: str) -> Dict[str, str]:
        """
        Parse the reflection response into a dictionary of suggestions.

        Args:
            response (str): The raw reflection response from the LLM.

        Returns:
            Dict[str, str]: A dictionary of parsed suggestions.

        Raises:
            ValueError: If the response cannot be parsed into suggestions.
        """
        suggestions = {}
        for line in response.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                suggestions[key.strip()] = value.strip()
        
        if not suggestions:
            raise ValueError("Unable to parse reflection response into suggestions")
        
        return suggestions
