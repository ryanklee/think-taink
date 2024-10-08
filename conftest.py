import sys
import os

# Add the src directory to the Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, src_path)

# Import the project_integrity_system package
from src.project_integrity_system import Axiom, Requirement, ProblemStatement
from src.project_integrity_system.document_types.base_document import BaseDocument as Document

# You can add any other necessary setup for your tests here

# Print the sys.path for debugging
print("Python path:")
print("\n".join(sys.path))
