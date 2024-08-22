import pytest
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

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

def test_process_empty_input(input_processor):
    input_text = ""
    expected_output = ""
    assert input_processor.process(input_text) == expected_output

def test_process_long_input(input_processor):
    input_text = " ".join(["word"] * 1000)
    expected_output = " ".join(["word"] * 1000)
    assert input_processor.process(input_text) == expected_output

def test_process_only_special_characters(input_processor):
    input_text = "@#$%^&*()_+"
    expected_output = ""
    assert input_processor.process(input_text) == expected_output
