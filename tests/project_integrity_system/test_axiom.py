import pytest
from src.project_integrity_system import Axiom, Requirement, ProblemStatement
from src.project_integrity_system import run_cli
from unittest.mock import patch
from io import StringIO

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

@pytest.fixture
def mock_input_files(tmp_path):
    axiom_file = tmp_path / "axiom.yaml"
    axiom_file.write_text("""
id: '@AXIOM-001'
description: Test axiom
linked_requirements:
  - '@REQ-001'
""")
    
    req_file = tmp_path / "requirement.yaml"
    req_file.write_text("""
id: '@REQ-001'
description: Test requirement
linked_problem_statements:
  - '@PROB-001'
linked_test_cases:
  - '@TEST-001'
""")
    
    prob_file = tmp_path / "problem.yaml"
    prob_file.write_text("""
id: '@PROB-001'
description: Test problem statement
linked_research_items:
  - '@RES-001'
linked_requirements:
  - '@REQ-001'
""")
    
    return [str(axiom_file), str(req_file), str(prob_file)]

def test_cli_validate(mock_input_files):
    with patch('sys.stdout', new=StringIO()) as fake_out:
        run_cli(['validate', '--input'] + mock_input_files)
        assert "No validation errors found." in fake_out.getvalue()

def test_cli_report(mock_input_files):
    with patch('sys.stdout', new=StringIO()) as fake_out:
        run_cli(['report', '--input'] + mock_input_files)
        output = fake_out.getvalue()
        assert "Project Document Summary" in output
        assert "Validation Report" in output
        assert "Total Documents: 3" in output
        assert "No errors found." in output

def test_cli_invalid_command():
    with pytest.raises(SystemExit):
        run_cli(['invalid_command'])

def test_cli_missing_input():
    with pytest.raises(SystemExit):
        run_cli(['validate'])
import pytest
from unittest.mock import patch
from io import StringIO
from src.project_integrity_system import run_cli

@pytest.fixture
def mock_input_files(tmp_path):
    axiom_file = tmp_path / "axiom.yaml"
    axiom_file.write_text("""
id: '@AXIOM-001'
description: Test axiom
linked_requirements:
  - '@REQ-001'
""")
    
    req_file = tmp_path / "requirement.yaml"
    req_file.write_text("""
id: '@REQ-001'
description: Test requirement
linked_problem_statements:
  - '@PROB-001'
linked_test_cases:
  - '@TEST-001'
""")
    
    prob_file = tmp_path / "problem.yaml"
    prob_file.write_text("""
id: '@PROB-001'
description: Test problem statement
linked_research_items:
  - '@RES-001'
linked_requirements:
  - '@REQ-001'
""")
    
    return [str(axiom_file), str(req_file), str(prob_file)]

def test_cli_validate(mock_input_files):
    with patch('sys.stdout', new=StringIO()) as fake_out:
        run_cli(['validate', '--input'] + mock_input_files)
        assert "No validation errors found." in fake_out.getvalue()

def test_cli_report(mock_input_files):
    with patch('sys.stdout', new=StringIO()) as fake_out:
        run_cli(['report', '--input'] + mock_input_files)
        output = fake_out.getvalue()
        assert "Project Document Summary" in output
        assert "Validation Report" in output
        assert "Total Documents: 3" in output
        assert "No errors found." in output

def test_cli_invalid_command():
    with pytest.raises(SystemExit):
        run_cli(['invalid_command'])

def test_cli_missing_input():
    with pytest.raises(SystemExit):
        run_cli(['validate'])
