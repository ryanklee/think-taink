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
        "llm": {
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 150,
            "api_key": "test_api_key"
        }
    }
    return LLMPool(config)

class TestLLMPool:
    @patch('src.llm_pool.llm_pool.AnthropicAPI')
    def test_generate_response_stream_success(self, mock_openai_api, llm_pool):
        log_stream = setup_logger()
        
        mock_generate_response_stream = MagicMock()
        mock_generate_response_stream.return_value = iter(["Test response"])
        mock_openai_api.return_value.generate_response_stream = mock_generate_response_stream
        mock_openai_api.return_value.is_test_environment = True
        llm_pool.api = mock_openai_api.return_value
        llm_pool.api.is_test_environment = True
        mock_openai_api.return_value.is_test_environment = True
        
        llm_pool.api = mock_openai_api.return_value
        
        input_text = "Test question"
        responses = list(llm_pool.generate_response_stream(input_text))
        
        assert len(responses) == 6  # 5 experts + 1 data usage note
        for response in responses[:-1]:  # Exclude the last response (data usage note)
            assert "expert" in response
            assert "response" in response
            assert response["response"] == "Test response"

        assert responses[-1]["expert"] == "System"
        assert "data sent to the openai api will not be used to train or improve openai models" in responses[-1]["response"].lower()

        assert mock_generate_response_stream.call_count == 5
        
        print(log_stream.getvalue())  # Print the captured logs

    @pytest.mark.parametrize("expert", ["Analyst", "Creative", "Critic", "Synthesizer", "Ethicist"])
    @patch('src.llm_pool.llm_pool.OpenAIAPI')
    def test_generate_response_stream_for_each_expert(self, mock_openai_api, expert, llm_pool):
        mock_generate_response_stream = MagicMock()
        mock_generate_response_stream.return_value = iter(["Test response"])
        mock_openai_api.return_value.generate_response_stream = mock_generate_response_stream
        mock_openai_api.return_value.is_test_environment = True

        llm_pool.api = mock_openai_api.return_value

        input_text = "Test question"
        responses = list(llm_pool.generate_response_stream(input_text))
        
        expert_response = next(r for r in responses if r["expert"] == expert)
        assert expert_response["response"] == "Test response"

    @patch('src.llm_pool.llm_pool.OpenAIAPI')
    def test_generate_response_stream_error_handling(self, mock_openai_api, llm_pool):
        mock_generate_response_stream = MagicMock()
        mock_generate_response_stream.side_effect = Exception("API Error")
        mock_openai_api.return_value.generate_response_stream = mock_generate_response_stream
        mock_openai_api.return_value.is_test_environment = False
        
        llm_pool.api = mock_openai_api.return_value
        
        input_text = "Test question"
        responses = list(llm_pool.generate_response_stream(input_text))
        
        assert len(responses) == 6  # 5 experts + 1 data usage note
        for response in responses[:-1]:  # Exclude the last response (data usage note)
            assert "expert" in response
            assert "response" in response
            assert "Error generating response: API Error" in response["response"]

        assert responses[-1]["expert"] == "System"
        assert "data sent to the openai api will not be used to train or improve openai models" in responses[-1]["response"].lower()

        assert mock_generate_response_stream.call_count == 5

    def test_llm_pool_configuration(self):
        config = {
            "llm": {
                "model": "gpt-4",
                "temperature": 0.5,
                "max_tokens": 200,
                "api_key": "test_api_key"
            }
        }
        llm_pool = LLMPool(config)
        
        assert llm_pool.api.model == "gpt-4"
        assert llm_pool.temperature == 0.5
        assert llm_pool.max_tokens == 200

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
        assert "TestExpert" in [expert["name"] for expert in llm_pool.experts]

        # Test adding a duplicate expert
        with pytest.raises(LLMPoolError):
            llm_pool.add_expert("TestExpert", "This is a duplicate expert.")

        # Test updating an expert
        llm_pool.update_expert("TestExpert", "This is an updated test expert.")
        updated_expert = next(expert for expert in llm_pool.experts if expert["name"] == "TestExpert")
        assert updated_expert["prompt"] == "This is an updated test expert."

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
