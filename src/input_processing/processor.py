import re

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
        """
        # Remove extra whitespace
        processed_text = ' '.join(input_text.split())
        
        # Remove special characters except for basic punctuation
        processed_text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', processed_text)
        
        return processed_text
