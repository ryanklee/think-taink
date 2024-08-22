import pytest
from unittest.mock import patch, MagicMock
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
    
    assert len(responses) == 3
    for response in responses:
        assert "expert" in response
        assert "response" in response
        assert response["response"] == "Mocked response"

    assert mock_create.call_count == 3

@patch('openai.Completion.create')
def test_generate_response_error_handling(mock_create, llm_pool):
    mock_create.side_effect = Exception("API Error")
    
    input_text = "Test question"
    responses = llm_pool.generate_response(input_text)
    
    assert len(responses) == 3
    for response in responses:
        assert "expert" in response
        assert "response" in response
        assert "Error generating response: API Error" in response["response"]

    assert mock_create.call_count == 3
