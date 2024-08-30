import sys
import os

# Add the src directory to the Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, src_path)

# Import the project_integrity_system package
from src.project_integrity_system import Axiom, Requirement, ProblemStatement
from src.project_integrity_system.document_types.base_document import BaseDocument as Document
from src.project_integrity_system.cli import main as cli_main

# You can add any other necessary setup for your tests here
