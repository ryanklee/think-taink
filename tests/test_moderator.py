import unittest
from unittest.mock import MagicMock, patch
import io
import logging
import time
from src.moderator.moderator import Moderator
from src.llm_pool.llm_pool import LLMPool
from src.heuristics.principles import Principles
from src.utils.exceptions import ModerationError

def setup_logger():
    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return log_stream

class TestModerator(unittest.TestCase):
    def setUp(self):
        self.llm_pool = MagicMock(spec=LLMPool)
        self.principles = MagicMock(spec=Principles)
        self.moderator = Moderator(self.llm_pool, self.principles)
        self.log_stream = setup_logger()

    def test_start_discussion(self):
        input_text = "What are the ethical implications of AI?"
        self.llm_pool.get_expert_names.return_value = ["Analyst", "Ethicist"]
        self.llm_pool.generate_response_stream.side_effect = [
            iter([{"expert": "Analyst", "response": "Sample response"}]),
            iter([{"expert": "Ethicist", "response": "Sample response"}]),
            iter([{"expert": "System", "response": "Summary of discussion"}]),
            iter([{"expert": "Analyst", "response": "Sample response"}]),
            iter([{"expert": "Ethicist", "response": "Sample response"}]),
            iter([{"expert": "System", "response": "Final summary"}]),
        ]
        self.principles.evaluate_response.return_value = {"relevance": 0.8, "originality": 0.7}

        start_time = time.time()
        discussion = []
        for response in self.moderator.start_discussion_stream(input_text):
            discussion.append(response)
            if time.time() - start_time > 10:  # 10 second timeout
                self.fail("Test timed out")

        self.assertEqual(len(discussion), 4)  # 2 experts * 2 turns
        self.assertEqual(self.moderator.current_turn, 4)
        self.llm_pool.generate_response_stream.assert_called()
        self.principles.evaluate_response.assert_called()
        
        print(self.log_stream.getvalue())  # Print the captured logs

    def test_start_discussion_error_handling(self):
        input_text = "What are the ethical implications of AI?"
        self.llm_pool.get_expert_names.return_value = ["Analyst", "Ethicist"]
        self.llm_pool.generate_response_stream.side_effect = Exception("API Error")

        with self.assertRaises(ModerationError):
            list(self.moderator.start_discussion_stream(input_text))

    def test_summarize_discussion(self):
        discussion = [
            {"expert": "Analyst", "response": "We should consider the economic impact."},
            {"expert": "Ethicist", "response": "We must prioritize fairness and transparency."}
        ]
        self.llm_pool.generate_response_stream.return_value = iter([{"expert": "System", "response": "Summary of the discussion"}])

        summary = self.moderator.summarize_discussion(discussion)

        self.assertEqual(summary, "Summary of the discussion")
        self.llm_pool.generate_response_stream.assert_called_once()

    def test_intervene(self):
        discussion = [
            {"expert": "Analyst", "response": "Off-topic response"},
            {"expert": "Ethicist", "response": "Another off-topic response"}
        ]
        self.llm_pool.generate_response_stream.return_value = iter([{"expert": "System", "response": "Let's refocus on the main topic"}])

        intervention = self.moderator.intervene(discussion)

        self.assertEqual(intervention, "Let's refocus on the main topic")
        self.llm_pool.generate_response_stream.assert_called_once()

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

if __name__ == '__main__':
    unittest.main()
