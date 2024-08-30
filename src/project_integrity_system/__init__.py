from .document_types.axiom import Axiom
from .document_types.requirement import Requirement
from .document_types.problem_statement import ProblemStatement
from .integrity_checker import IntegrityChecker
from .cli import main as cli_main

__all__ = ['Axiom', 'Requirement', 'ProblemStatement', 'IntegrityChecker', 'cli_main']

# Add version information
__version__ = '0.3.2'
import argparse
import sys
from typing import List
from .integrity_checker import IntegrityChecker
from .document_types import Axiom, Requirement, ProblemStatement

def parse_arguments(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Project Integrity System CLI")
    parser.add_argument('command', choices=['validate', 'report'], help='Command to execute')
    parser.add_argument('--input', '-i', nargs='+', required=True, help='Input YAML files')
    parser.add_argument('--output', '-o', help='Output file for report')
    return parser.parse_args(args)

def load_documents(file_paths: List[str]) -> List[dict]:
    documents = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            yaml_content = file.read()
            if yaml_content.startswith('@AXIOM-'):
                documents.append(Axiom.from_yaml(yaml_content))
            elif yaml_content.startswith('@REQ-'):
                documents.append(Requirement.from_yaml(yaml_content))
            elif yaml_content.startswith('@PROB-'):
                documents.append(ProblemStatement.from_yaml(yaml_content))
            else:
                raise ValueError(f"Unknown document type in file: {file_path}")
    return documents

def run_cli(args: List[str]) -> None:
    parsed_args = parse_arguments(args)
    
    checker = IntegrityChecker()
    documents = load_documents(parsed_args.input)
    for doc in documents:
        checker.add_document(doc)

    if parsed_args.command == 'validate':
        errors = checker.validate_all()
        if errors:
            print("Validation errors:")
            for error in errors:
                print(f"- {error}")
        else:
            print("No validation errors found.")
    elif parsed_args.command == 'report':
        report = checker.generate_full_report()
        if parsed_args.output:
            with open(parsed_args.output, 'w') as f:
                f.write(report)
            print(f"Report written to {parsed_args.output}")
        else:
            print(report)

def main():
    run_cli(sys.argv[1:])

if __name__ == "__main__":
    main()
import argparse
import sys
from typing import List
from .integrity_checker import IntegrityChecker
from .document_types import Axiom, Requirement, ProblemStatement

def parse_arguments(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Project Integrity System CLI")
    parser.add_argument('command', choices=['validate', 'report'], help='Command to execute')
    parser.add_argument('--input', '-i', nargs='+', required=True, help='Input YAML files')
    parser.add_argument('--output', '-o', help='Output file for report')
    return parser.parse_args(args)

def load_documents(file_paths: List[str]) -> List[dict]:
    documents = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            yaml_content = file.read()
            if yaml_content.startswith('@AXIOM-'):
                documents.append(Axiom.from_yaml(yaml_content))
            elif yaml_content.startswith('@REQ-'):
                documents.append(Requirement.from_yaml(yaml_content))
            elif yaml_content.startswith('@PROB-'):
                documents.append(ProblemStatement.from_yaml(yaml_content))
            else:
                raise ValueError(f"Unknown document type in file: {file_path}")
    return documents

def run_cli(args: List[str]) -> None:
    parsed_args = parse_arguments(args)
    
    checker = IntegrityChecker()
    documents = load_documents(parsed_args.input)
    for doc in documents:
        checker.add_document(doc)

    if parsed_args.command == 'validate':
        errors = checker.validate_all()
        if errors:
            print("Validation errors:")
            for error in errors:
                print(f"- {error}")
        else:
            print("No validation errors found.")
    elif parsed_args.command == 'report':
        report = checker.generate_full_report()
        if parsed_args.output:
            with open(parsed_args.output, 'w') as f:
                f.write(report)
            print(f"Report written to {parsed_args.output}")
        else:
            print(report)

def main():
    run_cli(sys.argv[1:])

if __name__ == "__main__":
    main()
