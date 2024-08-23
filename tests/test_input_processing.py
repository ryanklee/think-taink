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

def test_short_input_after_processing(input_processor):
    input_text = "a b c"
    with pytest.raises(InputProcessingError) as excinfo:
        input_processor.process(input_text)
    assert str(excinfo.value) == "Input text is too short. Minimum length is 5 characters."

def test_valid_short_input(input_processor):
    input_text = "abcde"
    processed = input_processor.process(input_text)
    assert processed == "abcde"

def test_process_long_input(input_processor):
    input_text = " ".join(["word"] * 1000)
    expected_output = " ".join(["word"] * 1000)
    assert input_processor.process(input_text) == expected_output

def test_process_only_special_characters(input_processor):
    input_text = "@#$%^&*()_+"
    expected_output = ""
    assert input_processor.process(input_text) == expected_output

def test_process_short_input_with_spaces(input_processor):
    input_text = "   a   "
    with pytest.raises(InputProcessingError) as excinfo:
        input_processor.process(input_text)
    assert str(excinfo.value) == "Input text is too short. Minimum length is 5 characters."
import unittest
from src.input_processing.processor import InputProcessor
from src.utils.exceptions import InputProcessingError

class TestInputProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = InputProcessor()

    def test_valid_input(self):
        input_text = "This is a valid input."
        processed = self.processor.process(input_text)
        self.assertEqual(processed, input_text)

    def test_empty_input(self):
        input_text = ""
        processed = self.processor.process(input_text)
        self.assertEqual(processed, "")

    def test_short_input_after_processing(self):
        input_text = "a b c"
        with self.assertRaises(InputProcessingError) as context:
            self.processor.process(input_text)
        self.assertEqual(str(context.exception), "Input text is too short. Minimum length is 5 characters.")

    def test_valid_short_input(self):
        input_text = "abcde"
        processed = self.processor.process(input_text)
        self.assertEqual(processed, "abcde")

    def test_input_with_extra_whitespace(self):
        input_text = "  This   has   extra   spaces.  "
        expected = "This has extra spaces."
        processed = self.processor.process(input_text)
        self.assertEqual(processed, expected)

    def test_input_with_special_characters(self):
        input_text = "This has @special# $characters%."
        expected = "This has special characters."
        processed = self.processor.process(input_text)
        self.assertEqual(processed, expected)

    def test_short_input(self):
        input_text = "Shrt"
        with self.assertRaises(InputProcessingError):
            self.processor.process(input_text)

    def test_empty_input(self):
        input_text = ""
        processed = self.processor.process(input_text)
        self.assertEqual(processed, "")

    def test_non_string_input(self):
        input_text = 12345
        with self.assertRaises(InputProcessingError):
            self.processor.process(input_text)

    def test_only_special_characters(self):
        input_text = "@#$%^&*()_+"
        processed = self.processor.process(input_text)
        self.assertEqual(processed, "")

    def test_short_input_with_spaces(self):
        input_text = "   a   "
        with self.assertRaises(InputProcessingError) as context:
            self.processor.process(input_text)
        self.assertEqual(str(context.exception), "Input text is too short. Minimum length is 5 characters.")

if __name__ == '__main__':
    unittest.main()
