import unittest
from unittest.mock import MagicMock, patch
from src.llm_pool.llm_pool import LLMPool
from src.llm_pool.pool_evolution import PoolEvolution

class TestPoolEvolution(unittest.TestCase):
    def setUp(self):
        self.llm_pool = MagicMock(spec=LLMPool)
        self.pool_evolution = PoolEvolution(self.llm_pool)

    def test_evolve_pool(self):
        # Mock discussion history
        discussion_history = [
            {"expert": "Analyst", "response": "We need more focus on technological trends."},
            {"expert": "Ethicist", "response": "We should consider adding an expert on emerging technologies."},
        ]

        # Mock LLM response
        self.llm_pool.generate_response_stream.return_value = iter([{"expert": "System", "response": "Add: Tech Futurist: An expert on emerging technologies and their potential impacts."}])

        self.pool_evolution.evolve_pool(discussion_history)

        # Check if add_expert was called with the correct arguments
        self.llm_pool.add_expert.assert_called_once_with("Tech Futurist", "An expert on emerging technologies and their potential impacts.")

    def test_generate_evolution_prompt(self):
        discussion_history = [
            {"expert": "Analyst", "response": "We need more focus on technological trends."},
        ]

        prompt = self.pool_evolution._generate_evolution_prompt(discussion_history)

        self.assertIn("Analyze the following discussion", prompt)
        self.assertIn("Analyst: We need more focus on technological trends.", prompt)
        self.assertIn("Current experts:", prompt)

    def test_parse_evolution_response(self):
        response = "Add: Tech Futurist: An expert on emerging technologies and their potential impacts.\nModify: Analyst: Focus more on technological trends and data analysis."
        parsed = self.pool_evolution._parse_evolution_response(response)

        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed["Tech Futurist"]["action"], "add")
        self.assertEqual(parsed["Analyst"]["action"], "modify")

    def test_apply_pool_changes(self):
        mock_llm_pool = MagicMock()
        pool_evolution = PoolEvolution(mock_llm_pool)

        suggestions = {
            "Tech Futurist": {"action": "add", "prompt": "An expert on emerging technologies."},
            "Analyst": {"action": "modify", "prompt": "Focus more on technological trends."},
            "Critic": {"action": "remove", "prompt": ""}
        }

        pool_evolution._apply_pool_changes(suggestions)

        mock_llm_pool.add_expert.assert_called_once_with("Tech Futurist", "An expert on emerging technologies.")
        mock_llm_pool.update_expert.assert_called_once_with("Analyst", "Focus more on technological trends.")
        mock_llm_pool.remove_expert.assert_called_once_with("Critic")

if __name__ == '__main__':
    unittest.main()
