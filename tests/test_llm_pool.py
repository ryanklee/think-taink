import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Mock openai module if it's not installed
try:
    import openai
except ImportError:
    openai = MagicMock()
    sys.modules['openai'] = openai

from src.llm_pool.llm_pool import LLMPool

@pytest.fixture
def llm_pool():
    config = {
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 150,
        "openai": {
            "api_key": "test_api_key"
        }
    }
    return LLMPool(config)

@patch('src.llm_pool.openai_api.OpenAIAPI.generate_response')
def test_generate_response(mock_generate_response, llm_pool):
    mock_generate_response.return_value = "Mocked response"
    
    input_text = "Test question"
    responses = llm_pool.generate_response(input_text)
    
    assert len(responses) == 5  # Updated to match the new number of experts
    for response in responses:
        assert "expert" in response
        assert "response" in response
        assert response["response"] == "Mocked response"

    assert mock_generate_response.call_count == 5  # Updated to match the new number of experts

@pytest.mark.parametrize("expert", ["Analyst", "Creative", "Critic", "Synthesizer", "Ethicist"])
def test_generate_response_for_each_expert(expert, llm_pool):
    with patch('src.llm_pool.openai_api.OpenAIAPI.generate_response') as mock_generate_response:
        mock_generate_response.return_value = f"{expert} response"
        
        input_text = "Test question"
        responses = llm_pool.generate_response(input_text)
        
        expert_response = next(r for r in responses if r["expert"] == expert)
        assert expert_response["response"] == f"{expert} response"

def test_llm_pool_configuration():
    config = {
        "model": "gpt-4",
        "temperature": 0.5,
        "max_tokens": 200,
        "openai": {
            "api_key": "test_api_key"
        }
    }
    llm_pool = LLMPool(config)
    
    assert llm_pool.api.model == "gpt-4"
    assert llm_pool.temperature == 0.5
    assert llm_pool.max_tokens == 200

@patch('src.llm_pool.openai_api.OpenAIAPI.generate_response')
def test_generate_response_error_handling(mock_generate_response, llm_pool):
    mock_generate_response.side_effect = Exception("API Error")
    
    input_text = "Test question"
    responses = llm_pool.generate_response(input_text)
    
    assert len(responses) == 5  # Updated to match the new number of experts
    for response in responses:
        assert "expert" in response
        assert "response" in response
        assert "API Error" in response["response"]

    assert mock_generate_response.call_count == 5  # Updated to match the new number of experts

def test_get_expert_names(llm_pool):
    expert_names = llm_pool.get_expert_names()
    assert expert_names == ["Analyst", "Creative", "Critic", "Synthesizer", "Ethicist"]

def test_get_expert_prompt(llm_pool):
    analyst_prompt = llm_pool.get_expert_prompt("Analyst")
    assert analyst_prompt == "You are an analytical expert. Provide a logical and data-driven perspective."

    with pytest.raises(ValueError):
        llm_pool.get_expert_prompt("NonexistentExpert")
import unittest
from unittest.mock import patch, MagicMock
from src.llm_pool.llm_pool import LLMPool
from src.utils.exceptions import LLMPoolError

class TestLLMPool(unittest.TestCase):
    def setUp(self):
        self.config = {
            'model': 'gpt-3.5-turbo',
            'temperature': 0.7,
            'max_tokens': 100,
            'openai': {
                'api_key': 'test_api_key'
            }
        }
        self.llm_pool = LLMPool(self.config)

    def test_add_expert(self):
        self.llm_pool.add_expert("TestExpert", "This is a test expert.")
        self.assertIn("TestExpert", [expert["name"] for expert in self.llm_pool.experts])

    def test_add_duplicate_expert(self):
        self.llm_pool.add_expert("TestExpert", "This is a test expert.")
        with self.assertRaises(LLMPoolError):
            self.llm_pool.add_expert("TestExpert", "This is a duplicate expert.")

    def test_remove_expert(self):
        self.llm_pool.add_expert("TestExpert", "This is a test expert.")
        self.llm_pool.remove_expert("TestExpert")
        self.assertNotIn("TestExpert", [expert["name"] for expert in self.llm_pool.experts])

    def test_remove_nonexistent_expert(self):
        with self.assertRaises(LLMPoolError):
            self.llm_pool.remove_expert("NonexistentExpert")

    def test_update_expert(self):
        self.llm_pool.add_expert("TestExpert", "This is a test expert.")
        self.llm_pool.update_expert("TestExpert", "This is an updated test expert.")
        updated_expert = next(expert for expert in self.llm_pool.experts if expert["name"] == "TestExpert")
        self.assertEqual(updated_expert["prompt"], "This is an updated test expert.")

    def test_update_nonexistent_expert(self):
        with self.assertRaises(LLMPoolError):
            self.llm_pool.update_expert("NonexistentExpert", "This expert doesn't exist.")

    @patch('openai.Completion.create')
    def test_generate_response(self, mock_create):
        mock_create.return_value = MagicMock(choices=[MagicMock(text="Test response")])
        responses = self.llm_pool.generate_response("Test input")
        self.assertEqual(len(responses), len(self.llm_pool.experts))
        for response in responses:
            self.assertIn("expert", response)
            self.assertIn("response", response)

    def test_get_expert_names(self):
        expert_names = self.llm_pool.get_expert_names()
        self.assertIsInstance(expert_names, list)
        self.assertEqual(len(expert_names), len(self.llm_pool.experts))

    def test_get_expert_prompt(self):
        expert_name = self.llm_pool.experts[0]["name"]
        prompt = self.llm_pool.get_expert_prompt(expert_name)
        self.assertIsInstance(prompt, str)

    def test_get_nonexistent_expert_prompt(self):
        with self.assertRaises(ValueError):
            self.llm_pool.get_expert_prompt("NonexistentExpert")

if __name__ == '__main__':
    unittest.main()
