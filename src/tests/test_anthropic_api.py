import pytest
from unittest.mock import patch, MagicMock
from src.llm_pool.anthropic_api import AnthropicAPI
from src.utils.exceptions import LLMPoolError

@pytest.fixture
def anthropic_api():
    return AnthropicAPI("test_api_key")

def test_init(anthropic_api):
    assert anthropic_api.api_key == "test_api_key"
    assert anthropic_api.model == "claude-3-sonnet-20240229"
    assert anthropic_api.is_test_environment == False

def test_rate_limit(anthropic_api):
    anthropic_api._rate_limit()
    assert anthropic_api.daily_request_count == 1
    
    # Test rate limit exception
    anthropic_api.daily_request_count = 1000
    with pytest.raises(LLMPoolError, match="Daily request limit exceeded"):
        anthropic_api._rate_limit()

@patch('anthropic.Anthropic')
def test_generate_response_stream(mock_anthropic, anthropic_api):
    mock_stream = MagicMock()
    mock_stream.text_stream = ["Test", "response"]
    mock_anthropic.return_value.messages.stream.return_value.__enter__.return_value = mock_stream

    result = list(anthropic_api.generate_response_stream("Test prompt"))
    assert result == ["Test", "response"]

@patch('anthropic.Anthropic')
def test_generate_chat_response(mock_anthropic, anthropic_api):
    mock_anthropic.return_value.messages.create.return_value.content = "Test chat response"

    result = anthropic_api.generate_chat_response([{"role": "user", "content": "Hello"}])
    assert result == "Test chat response"

@patch('anthropic.Anthropic')
def test_analyze_document(mock_anthropic, anthropic_api):
    mock_anthropic.return_value.messages.create.return_value.content = "Test document analysis"

    result = anthropic_api.analyze_document("Test document", "txt", "summary")
    assert result == {"analysis": "Test document analysis"}

def test_set_model(anthropic_api):
    anthropic_api.set_model("new-model")
    assert anthropic_api.model == "new-model"

@patch('anthropic.Anthropic')
def test_generate_response_stream_with_system_prompt(mock_anthropic, anthropic_api):
    mock_stream = MagicMock()
    mock_stream.text_stream = ["Test", "response"]
    mock_anthropic.return_value.messages.stream.return_value.__enter__.return_value = mock_stream

    result = list(anthropic_api.generate_response_stream("Test prompt", system_prompt="System instruction"))
    assert result == ["Test", "response"]
    mock_anthropic.return_value.messages.stream.assert_called_once_with(
        model=anthropic_api.model,
        max_tokens=4096,
        messages=[
            {"role": "system", "content": "System instruction"},
            {"role": "user", "content": "Test prompt"}
        ]
    )

@patch('anthropic.Anthropic')
def test_generate_chat_response_with_system_prompt(mock_anthropic, anthropic_api):
    mock_anthropic.return_value.messages.create.return_value.content = "Test chat response"

    result = anthropic_api.generate_chat_response(
        [{"role": "user", "content": "Hello"}],
        system_prompt="System instruction"
    )
    assert result == "Test chat response"
    mock_anthropic.return_value.messages.create.assert_called_once_with(
        model=anthropic_api.model,
        max_tokens=4096,
        messages=[
            {"role": "system", "content": "System instruction"},
            {"role": "user", "content": "Hello"}
        ]
    )

@patch('anthropic.Anthropic')
def test_analyze_document_with_system_prompt(mock_anthropic, anthropic_api):
    mock_anthropic.return_value.messages.create.return_value.content = "Test document analysis"

    result = anthropic_api.analyze_document("Test document", "txt", "summary", system_prompt="System instruction")
    assert result == {"analysis": "Test document analysis"}
    mock_anthropic.return_value.messages.create.assert_called_once_with(
        model=anthropic_api.model,
        messages=[
            {"role": "system", "content": "System instruction"},
            {"role": "user", "content": "Analyze this txt document. Perform a summary analysis:\n\nTest document"}
        ]
    )
