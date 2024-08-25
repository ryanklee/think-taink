import unittest
from unittest.mock import MagicMock, patch
from src.principles_evolution.reflector import Reflector
from src.heuristics.principles import Principles
from src.llm_pool.llm_pool import LLMPool
from src.utils.exceptions import ReflectionError

import tempfile
import os

class TestReflector(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.version_control_file = os.path.join(self.temp_dir, 'principles_version_control.json')
        self.principles = Principles(self.version_control_file)
        self.llm_pool = MagicMock(spec=LLMPool)
        self.reflector = Reflector(self.principles, self.llm_pool)

    def tearDown(self):
        os.remove(self.version_control_file)
        os.rmdir(self.temp_dir)

    def test_reflect_on_principles(self):
        # Mock discussion history
        discussion_history = [
            {"expert": "Analyst", "response": "We should focus more on data-driven decisions."},
            {"expert": "Creative", "response": "Let's not forget the importance of intuition and creativity."},
        ]

        # Mock LLM response
        self.llm_pool.generate_response_stream.return_value = iter([{"expert": "System", "response": "data_driven_decisions: Incorporate data analysis in decision-making processes.\nintuition: Value intuition alongside analytical thinking."}])

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

    @patch('src.heuristics.principles.Principles.apply_reflector_suggestions')
    def test_reflection_integration(self, mock_apply_suggestions):
        # Mock discussion history
        discussion_history = [
            {"expert": "Analyst", "response": "We need to consider long-term consequences more."},
            {"expert": "Ethicist", "response": "Ethical implications should be a primary concern."},
        ]

        # Mock LLM response
        self.llm_pool.generate_response_stream.return_value = iter([{"expert": "System", "response": "long_term_thinking: Consider long-term consequences in decision-making.\nethical_consideration: Prioritize ethical implications in all discussions."}])

        suggestions = self.reflector.reflect_on_principles(discussion_history)

        # Check if suggestions were generated correctly
        self.assertEqual(len(suggestions), 2)
        self.assertIn("long_term_thinking", suggestions)
        self.assertIn("ethical_consideration", suggestions)

        # Check if apply_reflector_suggestions was called with the correct arguments
        mock_apply_suggestions.assert_called_once_with(suggestions)

    def test_reflect_on_principles_error_handling(self):
        # Mock discussion history
        discussion_history = [
            {"expert": "Analyst", "response": "We should focus more on data-driven decisions."},
        ]

        # Mock LLM response to raise an exception
        self.llm_pool.generate_response_stream.side_effect = Exception("API Error")

        with self.assertRaises(ReflectionError):
            self.reflector.reflect_on_principles(discussion_history)

    def test_parse_reflection_response_error_handling(self):
        invalid_response = [{"response": "Invalid response format without colon"}]
        with self.assertRaises(ReflectionError):
            self.reflector._parse_reflection_response(invalid_response)

if __name__ == '__main__':
    unittest.main()
