import pytest
from unittest.mock import patch, MagicMock
from src.llm_pool.anthropic_api import AnthropicAPI
import sys
import io
import logging
from pathlib import Path
from src.llm_pool.llm_pool import LLMPool
from src.utils.exceptions import LLMPoolError

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Mock the anthropic module
sys.modules['anthropic'] = MagicMock()

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
        "anthropic": {
            "model": "claude-3-sonnet-20240229",
            "temperature": 0.7,
            "max_tokens": 150,
            "api_key": "test_anthropic_api_key"
        }
    }
    return LLMPool(config, api_type='anthropic')

class TestLLMPool:
    def test_generate_response_stream_success(self, llm_pool):
        log_stream = setup_logger()
    
        mock_generate_response_stream = MagicMock()
        mock_generate_response_stream.return_value = ["Test ", "response"]
        llm_pool.api_client.generate_response_stream = mock_generate_response_stream
    
        input_text = "Test question"
        responses = list(llm_pool.generate_response_stream(input_text))
    
        assert len(responses) == 11  # (5 experts * 2 chunks) + 1 data usage note
        for i, response in enumerate(responses[:-1]):  # Exclude the last response (data usage note)
            assert "expert" in response
            assert "response" in response
            if i % 2 == 0:
                assert response["response"] == "Test "
            else:
                assert response["response"] == "response"

        assert responses[-1]["expert"] == "System"
        assert "data sent to the" in responses[-1]["response"].lower()
        assert "api will be handled according to the provider's data retention policies" in responses[-1]["response"].lower()

        assert mock_generate_response_stream.call_count == 5
        
        print(log_stream.getvalue())  # Print the captured logs

    @pytest.mark.parametrize("expert", ["Analyst", "Creative", "Critic", "Synthesizer", "Ethicist"])
    def test_generate_response_stream_for_each_expert(self, expert, llm_pool):
        mock_generate_response_stream = MagicMock()
        mock_generate_response_stream.return_value = ["Test response"]
        llm_pool.api_client.generate_response_stream = mock_generate_response_stream
    
        input_text = "Test question"
        responses = list(llm_pool.generate_response_stream(input_text))
    
        expert_responses = [r for r in responses if r["expert"] == expert]
        assert len(expert_responses) == 1
        assert expert_responses[0]["response"] == "Test response"

    def test_generate_response_stream_error_handling(self, llm_pool):
        mock_generate_response_stream = MagicMock()
        mock_generate_response_stream.side_effect = Exception("API Error")
        llm_pool.api.generate_response_stream = mock_generate_response_stream

        input_text = "Test question"
        responses = list(llm_pool.generate_response_stream(input_text))

        assert len(responses) == 6  # 5 experts + 1 data usage note
        for response in responses[:-1]:  # Exclude the last response (data usage note)
            assert "expert" in response
            assert "response" in response
            assert "API Error" in response["response"]

        assert responses[-1]["expert"] == "System"
        assert "data sent to the" in responses[-1]["response"].lower()
        assert "api will be handled according to the provider's data retention policies" in responses[-1]["response"].lower()

        assert mock_generate_response_stream.call_count == 5

    def test_llm_pool_configuration(self, llm_pool):
        assert llm_pool.temperature == 0.7
        assert llm_pool.max_tokens == 4096

    def test_get_expert_names(self, llm_pool):
        expert_names = llm_pool.get_expert_names()
        assert expert_names == ["Analyst", "Creative", "Critic", "Synthesizer", "Ethicist"]

    def test_get_expert_prompt(self, llm_pool):
        analyst_prompt = llm_pool.get_expert_prompt("Analyst")
        assert analyst_prompt == "You are an analytical expert. Provide a logical and data-driven perspective."

        with pytest.raises(ValueError):
            llm_pool.get_expert_prompt("NonexistentExpert")

    def test_expert_management(self, llm_pool):
        # Test adding an expert
        llm_pool.add_expert("TestExpert", "This is a test expert.")
        assert "TestExpert" in llm_pool.get_expert_names()
    
        # Test adding a duplicate expert
        with pytest.raises(LLMPoolError):
            llm_pool.add_expert("TestExpert", "This is a duplicate expert.")
    
        # Test updating an expert
        llm_pool.update_expert("TestExpert", "This is an updated test expert.")
        updated_expert_prompt = llm_pool.get_expert_prompt("TestExpert")
        assert updated_expert_prompt == "This is an updated test expert."
    
        # Test removing an expert
        llm_pool.remove_expert("TestExpert")
        assert "TestExpert" not in [expert["name"] for expert in llm_pool.experts]

        # Test removing a nonexistent expert
        with pytest.raises(LLMPoolError):
            llm_pool.remove_expert("NonexistentExpert")

        # Test updating a nonexistent expert
        with pytest.raises(LLMPoolError):
            llm_pool.update_expert("NonexistentExpert", "This expert doesn't exist.")

if __name__ == '__main__':
    pytest.main()

import os
import pytest
from src.llm_pool.llm_pool import LLMPool

def test_llm_pool_initialization():
    # Ensure environment variable is set
    assert 'ANTHROPIC_API_KEY' in os.environ, "ANTHROPIC_API_KEY is not set in the environment"

    # Test Anthropic initialization
    anthropic_pool = LLMPool({})
    assert anthropic_pool.api_client.api.api_key == os.environ['ANTHROPIC_API_KEY']
