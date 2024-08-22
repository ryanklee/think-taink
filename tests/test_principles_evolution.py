import unittest
from unittest.mock import MagicMock
from src.principles_evolution.reflector import Reflector
from src.heuristics.principles import Principles
from src.llm_pool.llm_pool import LLMPool

class TestReflector(unittest.TestCase):
    def setUp(self):
        self.principles = Principles()
        self.llm_pool = MagicMock(spec=LLMPool)
        self.reflector = Reflector(self.principles, self.llm_pool)

    def test_reflect_on_principles(self):
        # Mock discussion history
        discussion_history = [
            {"expert": "Analyst", "response": "We should focus more on data-driven decisions."},
            {"expert": "Creative", "response": "Let's not forget the importance of intuition and creativity."},
        ]

        # Mock LLM response
        self.llm_pool.generate_response.return_value = "data_driven_decisions: Incorporate data analysis in decision-making processes.\nintuition: Value intuition alongside analytical thinking."

        suggestions = self.reflector.reflect_on_principles(discussion_history)

        self.assertEqual(len(suggestions), 2)
        self.assertIn("data_driven_decisions", suggestions)
        self.assertIn("intuition", suggestions)

    def test_generate_reflection_prompt(self):
        discussion_history = [
            {"expert": "Analyst", "response": "We should focus more on data-driven decisions."},
        ]

        prompt = self.reflector._generate_reflection_prompt(discussion_history)

        self.assertIn("Analyze the following discussion", prompt)
        self.assertIn("Analyst: We should focus more on data-driven decisions.", prompt)
        self.assertIn("Current principles:", prompt)

    def test_parse_reflection_response(self):
        response = "principle1: Description 1\nprinciple2: Description 2"
        parsed = self.reflector._parse_reflection_response(response)

        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed["principle1"], "Description 1")
        self.assertEqual(parsed["principle2"], "Description 2")

if __name__ == '__main__':
    unittest.main()
