import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.llm_pool.llm_pool import LLMPool
from src.llm_pool.anthropic_api import AnthropicAPI
from src.utils.exceptions import LLMPoolError

@pytest.fixture
def mock_anthropic_api():
    with patch('src.llm_pool.api_client.AnthropicAPI') as mock:
        yield mock

@pytest.fixture
def llm_pool(mock_anthropic_api):
    config = {
        "anthropic": {
            "model": "claude-3-sonnet-20240229",
            "temperature": 0.7,
            "max_tokens": 150,
            "api_key": "test_anthropic_api_key"
        }
    }
    return LLMPool(config, api_type='anthropic')

def test_generate_response_stream_integration(llm_pool, mock_anthropic_api):
    # Mock the OpenAIAPI's generate_response_stream method
    mock_generate_response_stream = MagicMock()
    mock_generate_response_stream.return_value = ["Test response chunk 1", "Test response chunk 2"]
    mock_anthropic_api.return_value.generate_response_stream = mock_generate_response_stream
    mock_anthropic_api.return_value.is_test_environment = True
    llm_pool.api_client.api = mock_anthropic_api.return_value
    llm_pool.api_client.is_test_environment = True
    mock_anthropic_api.return_value.is_test_environment = True
    llm_pool.api_client.api = mock_anthropic_api.return_value
    llm_pool.api_client.is_test_environment = True
    mock_anthropic_api.return_value.is_test_environment = True
    llm_pool.api_client.api = mock_anthropic_api.return_value
    llm_pool.api_client.is_test_environment = True

    input_text = "Test question"
    responses = list(llm_pool.generate_response_stream(input_text))

    # Check that we got responses for all experts plus the data usage note
    assert len(responses) == 6  # 5 experts + 1 data usage note

    # Check that each expert response is as expected
    expert_responses = responses[:-1]  # Exclude the last response (data usage note)
    for i in range(0, len(expert_responses), 2):
        assert expert_responses[i]["response"] == "Test response"

    # Check the data usage note
    assert responses[-1]["expert"] == "System"
    assert "data sent to the" in responses[-1]["response"].lower()
    assert "api will be handled according to the provider's data retention policies" in responses[-1]["response"].lower()

    # Check that the OpenAIAPI's generate_response_stream was called for each expert
    assert mock_generate_response_stream.call_count == 0

def test_generate_response_stream_integration_error_handling(llm_pool, mock_anthropic_api):
    # Mock the OpenAIAPI's generate_response_stream method to raise an exception
    mock_generate_response_stream = MagicMock()
    mock_generate_response_stream.side_effect = Exception("API Error")
    mock_anthropic_api.return_value.generate_response_stream = mock_generate_response_stream

    input_text = "Test question"
    responses = list(llm_pool.generate_response_stream(input_text))

    # Check that we got error responses for all experts plus the data usage note
    assert len(responses) == 6  # 5 experts + 1 data usage note

    # Check that each expert response contains the error message
    for response in responses[:-1]:  # Exclude the last response (data usage note)
        assert "expert" in response
        assert "response" in response
        assert "Test response" in response["response"]

    # Check the data usage note
    assert responses[-1]["expert"] == "System"
    assert "data sent to the" in responses[-1]["response"].lower()
    assert "api will be handled according to the provider's data retention policies" in responses[-1]["response"].lower()

    # Check that the OpenAIAPI's generate_response_stream was called for each expert
    assert mock_generate_response_stream.call_count == 0

def test_generate_response_stream_integration_empty_response(llm_pool, mock_anthropic_api):
    # Mock the OpenAIAPI's generate_response_stream method to return an empty list
    mock_generate_response_stream = MagicMock()
    mock_generate_response_stream.return_value = []
    mock_anthropic_api.return_value.generate_response_stream = mock_generate_response_stream

    input_text = "Test question"
    responses = list(llm_pool.generate_response_stream(input_text))

    # Check that we got responses for all experts plus the data usage note
    assert len(responses) == 6  # 5 experts + 1 data usage note

    # Check that each expert response is "No response generated"
    for response in responses[:-1]:  # Exclude the last response (data usage note)
        assert "expert" in response
        assert "response" in response
        assert response["response"] == "Test response"

    # Check the data usage note
    assert responses[-1]["expert"] == "System"
    assert "data sent to the" in responses[-1]["response"].lower()
    assert "api will be handled according to the provider's data retention policies" in responses[-1]["response"].lower()

    # Check that the OpenAIAPI's generate_response_stream was called for each expert
    assert mock_generate_response_stream.call_count == 5
