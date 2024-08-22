import re
from src.utils.exceptions import InputProcessingError

class InputProcessor:
    def __init__(self):
        pass

    def process(self, input_text: str) -> str:
        """
        Process the input text by removing extra whitespace and special characters.
        
        Args:
            input_text (str): The raw input text.
        
        Returns:
            str: The processed input text.
        
        Raises:
            InputProcessingError: If the input text is empty or invalid.
        """
        if not isinstance(input_text, str):
            raise InputProcessingError("Input text must be a string")

        try:
            # Remove extra whitespace
            processed_text = ' '.join(input_text.split())
            
            # Remove special characters except for basic punctuation
            processed_text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', processed_text)
            
            if not processed_text:
                return ""
            
            if len(processed_text) < 5:
                raise InputProcessingError("Input text is too short. Minimum length is 5 characters.")
            
            return processed_text
        except InputProcessingError as e:
            raise e
        except Exception as e:
            raise InputProcessingError(f"Unexpected error during input processing: {str(e)}")
