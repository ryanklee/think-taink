import pytest
from unittest.mock import patch, MagicMock
from src.llm_pool.llm_pool import LLMPool
from src.utils.exceptions import LLMPoolError

@pytest.fixture
def llm_pool():
    config = {
        'llm': {
            'default_api': 'anthropic',
            'temperature': 0.7,
            'max_tokens': 4096,
            'context_window': 128000
        },
        'anthropic': {
            'api_key': 'test_api_key'
        }
    }
    return LLMPool(config)

def test_init(llm_pool):
    assert llm_pool.api_type == 'anthropic'
    assert llm_pool.temperature == 0.7
    assert llm_pool.max_tokens == 4096
    assert llm_pool.context_window == 128000

@patch('src.llm_pool.api_client.APIClient.generate_response_stream')
def test_generate_response_stream(mock_generate_stream, llm_pool):
    mock_generate_stream.return_value = iter(["Test", "response"])
    
    result = list(llm_pool.generate_response_stream("Test input"))
    assert len(result) == 3  # 2 response chunks + 1 data usage note
    assert result[0]['expert'] == 'Analyst'
    assert result[0]['response'] == 'Test'
    assert result[1]['expert'] == 'Analyst'
    assert result[1]['response'] == 'response'
    assert result[2]['expert'] == 'System'
    assert 'Data sent to the ANTHROPIC API' in result[2]['response']

@patch('src.llm_pool.api_client.APIClient.generate_chat_response')
def test_generate_chat_response(mock_generate_chat, llm_pool):
    mock_generate_chat.return_value = "Test chat response"
    
    result = llm_pool.generate_chat_response([{"role": "user", "content": "Hello"}])
    assert result == "Test chat response"

@patch('src.llm_pool.api_client.APIClient.analyze_document')
def test_analyze_document(mock_analyze_document, llm_pool):
    mock_analyze_document.return_value = {"analysis": "Test document analysis"}
    
    result = llm_pool.analyze_document("Test document", "txt", "summary")
    assert result == {"analysis": "Test document analysis"}

def test_set_api_type(llm_pool):
    llm_pool.set_api_type('openai')
    assert llm_pool.api_type == 'openai'

    with pytest.raises(ValueError, match="Unsupported API type: invalid_api"):
        llm_pool.set_api_type('invalid_api')
