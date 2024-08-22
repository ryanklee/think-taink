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
        "max_tokens": 150
    }
    return LLMPool(config)

@patch('openai.Completion.create')
def test_generate_response(mock_create, llm_pool):
    mock_create.return_value = MagicMock(choices=[MagicMock(text="Mocked response")])
    
    input_text = "Test question"
    responses = llm_pool.generate_response(input_text)
    
    assert len(responses) == 5  # Updated to match the new number of experts
    for response in responses:
        assert "expert" in response
        assert "response" in response
        assert response["response"] == "Mocked response"

    assert mock_create.call_count == 5  # Updated to match the new number of experts

@pytest.mark.parametrize("expert", ["Analyst", "Creative", "Critic", "Synthesizer", "Ethicist"])
def test_generate_response_for_each_expert(expert, llm_pool):
    with patch('openai.Completion.create') as mock_create:
        mock_create.return_value = MagicMock(choices=[MagicMock(text=f"{expert} response")])
        
        input_text = "Test question"
        responses = llm_pool.generate_response(input_text)
        
        expert_response = next(r for r in responses if r["expert"] == expert)
        assert expert_response["response"] == f"{expert} response"

def test_llm_pool_configuration():
    config = {
        "model": "gpt-4",
        "temperature": 0.5,
        "max_tokens": 200
    }
    llm_pool = LLMPool(config)
    
    assert llm_pool.model == "gpt-4"
    assert llm_pool.temperature == 0.5
    assert llm_pool.max_tokens == 200

@patch('openai.Completion.create')
def test_generate_response_error_handling(mock_create, llm_pool):
    mock_create.side_effect = Exception("API Error")
    
    input_text = "Test question"
    responses = llm_pool.generate_response(input_text)
    
    assert len(responses) == 5  # Updated to match the new number of experts
    for response in responses:
        assert "expert" in response
        assert "response" in response
        assert "Error generating response: API Error" in response["response"]

    assert mock_create.call_count == 5  # Updated to match the new number of experts

def test_get_expert_names(llm_pool):
    expert_names = llm_pool.get_expert_names()
    assert expert_names == ["Analyst", "Creative", "Critic", "Synthesizer", "Ethicist"]

def test_get_expert_prompt(llm_pool):
    analyst_prompt = llm_pool.get_expert_prompt("Analyst")
    assert analyst_prompt == "You are an analytical expert. Provide a logical and data-driven perspective."

    with pytest.raises(ValueError):
        llm_pool.get_expert_prompt("NonexistentExpert")
