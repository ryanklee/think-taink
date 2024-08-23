import unittest
from unittest.mock import MagicMock, patch
from src.moderator.moderator import Moderator
from src.llm_pool.llm_pool import LLMPool
from src.heuristics.principles import Principles
from src.utils.exceptions import ModerationError

class TestModerator(unittest.TestCase):
    def setUp(self):
        self.llm_pool = MagicMock(spec=LLMPool)
        self.principles = MagicMock(spec=Principles)
        self.moderator = Moderator(self.llm_pool, self.principles)

    def test_start_discussion(self):
        input_text = "What are the ethical implications of AI?"
        self.llm_pool.get_expert_names.return_value = ["Analyst", "Ethicist"]
        self.llm_pool.generate_response.return_value = [{"response": "Sample response"}]
        self.principles.evaluate_response.return_value = {"relevance": 0.8, "originality": 0.7}

        discussion = self.moderator.start_discussion(input_text)

        self.assertEqual(len(discussion), 2)  # Two experts
        self.assertEqual(self.moderator.current_turn, 2)
        self.llm_pool.generate_response.assert_called()
        self.principles.evaluate_response.assert_called()

    def test_summarize_discussion(self):
        discussion = [
            {"expert": "Analyst", "response": "We should consider the economic impact."},
            {"expert": "Ethicist", "response": "We must prioritize fairness and transparency."}
        ]
        self.llm_pool.generate_response.return_value = [{"response": "Summary of the discussion"}]

        summary = self.moderator.summarize_discussion(discussion)

        self.assertEqual(summary, "Summary of the discussion")
        self.llm_pool.generate_response.assert_called_once()

    def test_intervene(self):
        discussion = [
            {"expert": "Analyst", "response": "Off-topic response"},
            {"expert": "Ethicist", "response": "Another off-topic response"}
        ]
        self.llm_pool.generate_response.return_value = [{"response": "Let's refocus on the main topic"}]

        intervention = self.moderator.intervene(discussion)

        self.assertEqual(intervention, [{"response": "Let's refocus on the main topic"}])
        self.llm_pool.generate_response.assert_called_once()

    @patch('src.principles_evolution.reflector.Reflector.reflect_on_principles')
    def test_reflect_on_principles(self, mock_reflect):
        discussion = [
            {"expert": "Analyst", "response": "We should consider the economic impact."},
            {"expert": "Ethicist", "response": "We must prioritize fairness and transparency."}
        ]
        mock_reflect.return_value = {"new_principle": "Consider both economic and ethical impacts"}

        self.moderator._reflect_on_principles(discussion)

        mock_reflect.assert_called_once_with(discussion)
        self.principles.apply_reflector_suggestions.assert_called_once_with({"new_principle": "Consider both economic and ethical impacts"})

    @patch('src.llm_pool.pool_evolution.PoolEvolution.evolve_pool')
    def test_evolve_expert_pool(self, mock_evolve):
        discussion = [
            {"expert": "Analyst", "response": "We should consider the economic impact."},
            {"expert": "Ethicist", "response": "We must prioritize fairness and transparency."}
        ]

        self.moderator._evolve_expert_pool(discussion)

        mock_evolve.assert_called_once_with(discussion)

    def test_start_discussion_error_handling(self):
        input_text = "What are the ethical implications of AI?"
        self.llm_pool.generate_response.side_effect = Exception("API Error")

        with self.assertRaises(ModerationError):
            self.moderator.start_discussion(input_text)

if __name__ == '__main__':
    unittest.main()