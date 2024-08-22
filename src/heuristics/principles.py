from typing import Dict

from typing import Dict
import logging

class Principles:
    def __init__(self):
        self.principles = {
            "intellectual_honesty": "Strive for truthfulness and objectivity in all discussions.",
            "critical_thinking": "Analyze arguments and evidence carefully before drawing conclusions.",
            "creativity": "Encourage novel and innovative ideas.",
            "diversity_of_thought": "Value and consider different perspectives and viewpoints."
        }

    def evaluate_response(self, response: str) -> Dict[str, float]:
        """
        Evaluate a response based on the current principles.

        Args:
            response (str): The response to evaluate.

        Returns:
            Dict[str, float]: A dictionary of principle scores.
        """
        # TODO: Implement a more sophisticated evaluation method
        # For now, we'll use a simple keyword-based scoring system
        scores = {}
        for principle, description in self.principles.items():
            keywords = description.lower().split()
            score = sum(1 for keyword in keywords if keyword in response.lower())
            scores[principle] = score / len(keywords)
        return scores

    def get_principles(self) -> Dict[str, str]:
        """
        Get the current principles.

        Returns:
            Dict[str, str]: A dictionary of principle names and descriptions.
        """
        return self.principles

    def add_principle(self, name: str, description: str) -> None:
        """
        Add a new principle.

        Args:
            name (str): The name of the new principle.
            description (str): The description of the new principle.
        """
        self.principles[name] = description
        logging.info(f"Added new principle: {name}")

    def remove_principle(self, name: str) -> None:
        """
        Remove a principle.

        Args:
            name (str): The name of the principle to remove.
        """
        if name in self.principles:
            del self.principles[name]
            logging.info(f"Removed principle: {name}")
        else:
            logging.warning(f"Attempted to remove non-existent principle: {name}")

    def update_principle(self, name: str, new_description: str) -> None:
        """
        Update an existing principle.

        Args:
            name (str): The name of the principle to update.
            new_description (str): The new description for the principle.
        """
        if name in self.principles:
            self.principles[name] = new_description
            logging.info(f"Updated principle: {name}")
        else:
            logging.warning(f"Attempted to update non-existent principle: {name}")

    def apply_reflector_suggestions(self, suggestions: Dict[str, str]) -> None:
        """
        Apply suggestions from the reflector to update principles.

        Args:
            suggestions (Dict[str, str]): A dictionary of principle names and suggested descriptions.
        """
        for name, suggestion in suggestions.items():
            if name in self.principles:
                self.update_principle(name, suggestion)
            else:
                self.add_principle(name, suggestion)
        logging.info(f"Applied {len(suggestions)} reflector suggestions")
