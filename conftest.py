import sys
import os

# Add the src directory to the Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, src_path)

print(f"Python path: {sys.path}")

# Import the project_integrity_system package
import project_integrity_system

print(f"project_integrity_system path: {project_integrity_system.__file__}")
print(f"project_integrity_system contents: {dir(project_integrity_system)}")

from project_integrity_system import Axiom
print(f"Axiom class: {Axiom}")
