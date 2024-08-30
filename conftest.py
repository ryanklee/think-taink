import sys
import os

# Add the src directory to the Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, src_path)

# Import the project_integrity_system package
from project_integrity_system.document_types import Axiom, Requirement, ProblemStatement, BaseDocument

# You can add any other necessary setup for your tests here
