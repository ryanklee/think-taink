import pytest
from unittest.mock import patch, MagicMock
import sys
import io
import logging
from pathlib import Path
from src.llm_pool.llm_pool import LLMPool
from src.utils.exceptions import LLMPoolError

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Mock the entire openai module
sys.modules['openai'] = MagicMock()

# Set up logging
def setup_logger():
    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return log_stream

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

@patch('src.llm_pool.llm_pool.OpenAIAPI')
def test_generate_response_stream(mock_openai_api, llm_pool):
    log_stream = setup_logger()
    
    mock_generate_response_stream = MagicMock()
    mock_generate_response_stream.return_value = iter(["Test response"])
    mock_openai_api.return_value.generate_response_stream = mock_generate_response_stream
    mock_openai_api.return_value.is_test_environment = True
    
    # Replace the OpenAIAPI instance in llm_pool with our mock
    llm_pool.api = mock_openai_api.return_value
    
    input_text = "Test question"
    responses = list(llm_pool.generate_response_stream(input_text))
    
    assert len(responses) == 6  # 5 experts + 1 data usage note
    for response in responses[:-1]:  # Exclude the last response (data usage note)
        assert "expert" in response
        assert "response" in response
        assert response["response"] == "Test response"

    # Check the data usage note
    assert responses[-1]["expert"] == "System"
    assert "data sent to the openai api will not be used to train or improve openai models" in responses[-1]["response"].lower()

    assert mock_generate_response_stream.call_count == 5  # The number of expert calls remains the same
    
    print(log_stream.getvalue())  # Print the captured logs

@pytest.mark.parametrize("expert", ["Analyst", "Creative", "Critic", "Synthesizer", "Ethicist"])
@patch('src.llm_pool.llm_pool.OpenAIAPI')
def test_generate_response_stream_for_each_expert(mock_openai_api, expert, llm_pool):
    mock_generate_response_stream = MagicMock()
    mock_generate_response_stream.return_value = iter(["Test response"])
    mock_openai_api.return_value.generate_response_stream = mock_generate_response_stream
    mock_openai_api.return_value.is_test_environment = True

    # Replace the OpenAIAPI instance in llm_pool with our mock
    llm_pool.api = mock_openai_api.return_value

    input_text = "Test question"
    responses = list(llm_pool.generate_response_stream(input_text))
    
    expert_response = next(r for r in responses if r["expert"] == expert)
    assert expert_response["response"] == "Test response"

@patch('src.llm_pool.llm_pool.OpenAIAPI')
def test_generate_response_stream_error_handling(mock_openai_api, llm_pool):
    mock_generate_response_stream = MagicMock()
    mock_generate_response_stream.side_effect = Exception("API Error")
    mock_openai_api.return_value.generate_response_stream = mock_generate_response_stream
    mock_openai_api.return_value.is_test_environment = False
    
    # Replace the OpenAIAPI instance in llm_pool with our mock
    llm_pool.api = mock_openai_api.return_value
    
    input_text = "Test question"
    responses = list(llm_pool.generate_response_stream(input_text))
    
    assert len(responses) == 6  # 5 experts + 1 data usage note
    for response in responses[:-1]:  # Exclude the last response (data usage note)
        assert "expert" in response
        assert "response" in response
        assert "Error generating response: API Error" in response["response"]

    # Check the data usage note
    assert responses[-1]["expert"] == "System"
    assert "data sent to the openai api will not be used to train or improve openai models" in responses[-1]["response"].lower()

    assert mock_generate_response_stream.call_count == 5  # The number of expert calls remains the same

@pytest.mark.parametrize("expert", ["Analyst", "Creative", "Critic", "Synthesizer", "Ethicist"])
@patch('src.llm_pool.openai_api.OpenAIAPI')
def test_generate_response_stream_for_each_expert(mock_openai_api, expert, llm_pool):
    mock_generate_response_stream = MagicMock()
    mock_generate_response_stream.return_value = iter(["Test response"])
    mock_openai_api.return_value.generate_response_stream = mock_generate_response_stream
    mock_openai_api.return_value.is_test_environment = True

    input_text = "Test question"
    responses = list(llm_pool.generate_response_stream(input_text))
    
    expert_response = next(r for r in responses if r["expert"] == expert)
    assert expert_response["response"] == "Test response"

@patch('src.llm_pool.openai_api.OpenAIAPI')
def test_llm_pool_configuration(mock_openai_api):
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

@patch('src.llm_pool.openai_api.OpenAIAPI')
def test_generate_response_stream_error_handling(mock_openai_api, llm_pool):
    mock_generate_response_stream = MagicMock()
    mock_generate_response_stream.side_effect = Exception("API Error")
    mock_openai_api.return_value.generate_response_stream = mock_generate_response_stream
    
    input_text = "Test question"
    responses = list(llm_pool.generate_response_stream(input_text))
    
    assert len(responses) == 6  # Updated to include the data usage note
    for response in responses[:-1]:  # Exclude the last response (data usage note)
        assert "expert" in response
        assert "response" in response
        assert "API Error" in response["response"]

    # Check the data usage note
    assert responses[-1]["expert"] == "System"
    assert "data sent to the openai api will not be used to train or improve openai models" in responses[-1]["response"].lower()

    assert mock_generate_response_stream.call_count == 5  # The number of expert calls remains the same

def test_get_expert_names(llm_pool):
    expert_names = llm_pool.get_expert_names()
    assert expert_names == ["Analyst", "Creative", "Critic", "Synthesizer", "Ethicist"]

def test_get_expert_prompt(llm_pool):
    analyst_prompt = llm_pool.get_expert_prompt("Analyst")
    assert analyst_prompt == "You are an analytical expert. Provide a logical and data-driven perspective."

    with pytest.raises(ValueError):
        llm_pool.get_expert_prompt("NonexistentExpert")

def test_add_expert(llm_pool):
    llm_pool.add_expert("TestExpert", "This is a test expert.")
    assert "TestExpert" in [expert["name"] for expert in llm_pool.experts]

def test_add_duplicate_expert(llm_pool):
    llm_pool.add_expert("TestExpert", "This is a test expert.")
    with pytest.raises(LLMPoolError):
        llm_pool.add_expert("TestExpert", "This is a duplicate expert.")

def test_remove_expert(llm_pool):
    llm_pool.add_expert("TestExpert", "This is a test expert.")
    llm_pool.remove_expert("TestExpert")
    assert "TestExpert" not in [expert["name"] for expert in llm_pool.experts]

def test_remove_nonexistent_expert(llm_pool):
    with pytest.raises(LLMPoolError):
        llm_pool.remove_expert("NonexistentExpert")

def test_update_expert(llm_pool):
    llm_pool.add_expert("TestExpert", "This is a test expert.")
    llm_pool.update_expert("TestExpert", "This is an updated test expert.")
    updated_expert = next(expert for expert in llm_pool.experts if expert["name"] == "TestExpert")
    assert updated_expert["prompt"] == "This is an updated test expert."

def test_update_nonexistent_expert(llm_pool):
    with pytest.raises(LLMPoolError):
        llm_pool.update_expert("NonexistentExpert", "This expert doesn't exist.")

if __name__ == '__main__':
    pytest.main()
