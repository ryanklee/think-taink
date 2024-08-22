import pytest
from src.input_processing.processor import InputProcessor

@pytest.fixture
def input_processor():
    return InputProcessor()

def test_process_removes_extra_whitespace(input_processor):
    input_text = "  This   is  a   test  "
    expected_output = "This is a test"
    assert input_processor.process(input_text) == expected_output

def test_process_removes_special_characters(input_processor):
    input_text = "Hello, world! This is a test@#$%^&*()_+"
    expected_output = "Hello, world! This is a test"
    assert input_processor.process(input_text) == expected_output

def test_process_preserves_basic_punctuation(input_processor):
    input_text = "Hello, world! This is a test."
    expected_output = "Hello, world! This is a test."
    assert input_processor.process(input_text) == expected_output
