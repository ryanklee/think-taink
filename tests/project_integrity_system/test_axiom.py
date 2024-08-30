import pytest
from src.project_integrity_system import Axiom, Requirement, ProblemStatement

def test_axiom():
    data = {
        'id': '@AXIOM-001',
        'description': 'Test axiom',
        'linked_requirements': ['@REQ-001']
    }
    axiom = Axiom(data)
    assert axiom.id == '@AXIOM-001'
    assert axiom.description == 'Test axiom'
    assert axiom.linked_requirements == ['@REQ-001']
    assert axiom.get_linked_ids() == ['@REQ-001']
    assert axiom.get_document_type() == "Axiom"
    axiom.validate()  # Should not raise an exception

    invalid_axiom = Axiom({'id': 'INVALID-001', 'description': 'Test axiom', 'linked_requirements': []})
    errors = invalid_axiom.validate()
    assert len(errors) > 0
    assert any("Invalid Axiom ID" in error for error in errors)

def test_requirement():
    data = {
        'id': '@REQ-001',
        'description': 'Test requirement',
        'linked_problem_statements': ['@PROB-001'],
        'linked_test_cases': ['@TEST-001']
    }
    req = Requirement(data)
    assert req.id == '@REQ-001'
    assert req.description == 'Test requirement'
    assert req.linked_problem_statements == ['@PROB-001']
    assert req.linked_test_cases == ['@TEST-001']
    assert set(req.get_linked_ids()) == {'@PROB-001', '@TEST-001'}
    assert req.get_document_type() == "Requirement"
    req.validate()  # Should not raise an exception

    invalid_req = Requirement({'id': '@REQ-001', 'description': 'Test requirement', 'linked_problem_statements': [], 'linked_test_cases': []})
    errors = invalid_req.validate()
    assert len(errors) > 0
    assert any("has no linked problem statements" in error for error in errors)
    assert any("has no linked test cases" in error for error in errors)

def test_problem_statement():
    data = {
        'id': '@PROB-001',
        'description': 'Test problem statement',
        'linked_research_items': ['@RES-001'],
        'linked_requirements': ['@REQ-001']
    }
    prob = ProblemStatement(data)
    assert prob.id == '@PROB-001'
    assert prob.description == 'Test problem statement'
    assert prob.linked_research_items == ['@RES-001']
    assert prob.linked_requirements == ['@REQ-001']
    assert set(prob.get_linked_ids()) == {'@RES-001', '@REQ-001'}
    assert prob.get_document_type() == "ProblemStatement"
    prob.validate()  # Should not raise an exception

    invalid_prob = ProblemStatement({'id': '@PROB-001', 'description': 'Test problem', 'linked_research_items': [], 'linked_requirements': []})
    errors = invalid_prob.validate()
    assert len(errors) > 0
    assert any("has no linked research items" in error for error in errors)
    assert any("has no linked requirements" in error for error in errors)

def test_from_yaml():
    yaml_string = """
    id: '@AXIOM-001'
    description: Test axiom
    linked_requirements:
      - '@REQ-001'
    """
    axiom = Axiom.from_yaml(yaml_string)
    assert axiom.id == '@AXIOM-001'
    assert axiom.description == 'Test axiom'
    assert axiom.linked_requirements == ['@REQ-001']
import pytest
from unittest.mock import patch, mock_open
from src.project_integrity_system.cli import parse_arguments, load_documents, run_cli
from src.project_integrity_system.document_types import Axiom, Requirement, ProblemStatement

def test_parse_arguments():
    args = ['validate', '-i', 'file1.yaml', 'file2.yaml']
    parsed_args = parse_arguments(args)
    assert parsed_args.command == 'validate'
    assert parsed_args.input == ['file1.yaml', 'file2.yaml']
    assert parsed_args.output is None

    args = ['report', '-i', 'file1.yaml', '-o', 'report.txt']
    parsed_args = parse_arguments(args)
    assert parsed_args.command == 'report'
    assert parsed_args.input == ['file1.yaml']
    assert parsed_args.output == 'report.txt'

def test_load_documents():
    mock_yaml_content = {
        'axiom.yaml': '@AXIOM-001:\n  description: Test Axiom\n  linked_requirements: [@REQ-001]',
        'requirement.yaml': '@REQ-001:\n  description: Test Requirement\n  linked_problem_statements: [@PROB-001]\n  linked_test_cases: [@TEST-001]',
        'problem.yaml': '@PROB-001:\n  description: Test Problem\n  linked_research_items: [@RES-001]\n  linked_requirements: [@REQ-001]'
    }

    with patch('builtins.open', mock_open()) as mock_file:
        mock_file.side_effect = lambda file, mode: mock_open(read_data=mock_yaml_content[file]).return_value

        documents = load_documents(['axiom.yaml', 'requirement.yaml', 'problem.yaml'])

    assert len(documents) == 3
    assert isinstance(documents[0], Axiom)
    assert isinstance(documents[1], Requirement)
    assert isinstance(documents[2], ProblemStatement)

@patch('src.project_integrity_system.cli.IntegrityChecker')
@patch('src.project_integrity_system.cli.load_documents')
def test_run_cli_validate(mock_load_documents, mock_integrity_checker):
    mock_load_documents.return_value = [
        Axiom({'id': '@AXIOM-001', 'description': 'Test Axiom', 'linked_requirements': ['@REQ-001']}),
        Requirement({'id': '@REQ-001', 'description': 'Test Requirement', 'linked_problem_statements': ['@PROB-001'], 'linked_test_cases': ['@TEST-001']}),
        ProblemStatement({'id': '@PROB-001', 'description': 'Test Problem', 'linked_research_items': ['@RES-001'], 'linked_requirements': ['@REQ-001']})
    ]

    mock_checker = mock_integrity_checker.return_value
    mock_checker.validate_all.return_value = []

    with patch('sys.stdout') as mock_stdout:
        run_cli(['validate', '-i', 'file1.yaml', 'file2.yaml'])

    mock_checker.validate_all.assert_called_once()
    mock_stdout.write.assert_called_with("No validation errors found.\n")

@patch('src.project_integrity_system.cli.IntegrityChecker')
@patch('src.project_integrity_system.cli.load_documents')
def test_run_cli_report(mock_load_documents, mock_integrity_checker):
    mock_load_documents.return_value = [
        Axiom({'id': '@AXIOM-001', 'description': 'Test Axiom', 'linked_requirements': ['@REQ-001']}),
        Requirement({'id': '@REQ-001', 'description': 'Test Requirement', 'linked_problem_statements': ['@PROB-001'], 'linked_test_cases': ['@TEST-001']}),
        ProblemStatement({'id': '@PROB-001', 'description': 'Test Problem', 'linked_research_items': ['@RES-001'], 'linked_requirements': ['@REQ-001']})
    ]

    mock_checker = mock_integrity_checker.return_value
    mock_checker.generate_full_report.return_value = "Test Report"

    with patch('builtins.open', mock_open()) as mock_file:
        run_cli(['report', '-i', 'file1.yaml', '-o', 'report.txt'])

    mock_checker.generate_full_report.assert_called_once()
    mock_file.assert_called_with('report.txt', 'w')
    mock_file().write.assert_called_with("Test Report")
