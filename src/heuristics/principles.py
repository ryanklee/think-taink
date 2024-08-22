from typing import Dict

class Principles:
    def __init__(self):
        self.principles = {
            "intellectual_honesty": "Strive for truthfulness and objectivity in all discussions.",
            "critical_thinking": "Analyze arguments and evidence carefully before drawing conclusions.",
            "creativity": "Encourage novel and innovative ideas.",
            "diversity_of_thought": "Value and consider different perspectives and viewpoints."
        }

    def evaluate_response(self, response: str) -> Dict[str, float]:
        # TODO: Implement a more sophisticated evaluation method
        # For now, we'll use a simple keyword-based scoring system
        scores = {}
        for principle, description in self.principles.items():
            keywords = description.lower().split()
            score = sum(1 for keyword in keywords if keyword in response.lower())
            scores[principle] = score / len(keywords)
        return scores

    def get_principles(self) -> Dict[str, str]:
        return self.principles

    def add_principle(self, name: str, description: str):
        self.principles[name] = description

    def remove_principle(self, name: str):
        if name in self.principles:
            del self.principles[name]

    def update_principle(self, name: str, new_description: str):
        if name in self.principles:
            self.principles[name] = new_description

    def apply_reflector_suggestions(self, suggestions: Dict[str, str]):
        for name, suggestion in suggestions.items():
            if name in self.principles:
                self.update_principle(name, suggestion)
            else:
                self.add_principle(name, suggestion)
