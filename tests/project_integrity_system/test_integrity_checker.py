import pytest
import logging
from src.project_integrity_system import IntegrityChecker, Axiom, Requirement, ProblemStatement

@pytest.fixture(autouse=True)
def setup_logging():
    logging.basicConfig(level=logging.DEBUG)

def test_integrity_checker(caplog):
    caplog.set_level(logging.DEBUG)
    
    checker = IntegrityChecker()

    # Create valid documents
    axiom = Axiom({'id': '@AXIOM-001', 'description': 'Test axiom', 'linked_requirements': ['@REQ-001']})
    requirement = Requirement({'id': '@REQ-001', 'description': 'Test requirement', 'linked_problem_statements': ['@PROB-001'], 'linked_test_cases': ['@TEST-001']})
    problem_statement = ProblemStatement({'id': '@PROB-001', 'description': 'Test problem', 'linked_research_items': ['@RES-001'], 'linked_requirements': ['@REQ-001']})

    checker.add_document(axiom)
    checker.add_document(requirement)
    checker.add_document(problem_statement)

    # Test valid configuration
    errors = checker.validate_all()
    assert errors == []
    assert "Starting validation of all documents" in caplog.text
    assert "Validation complete. Found 0 errors." in caplog.text

    # Test invalid cross-reference
    invalid_axiom = Axiom({'id': '@AXIOM-002', 'description': 'Invalid axiom', 'linked_requirements': ['@REQ-002']})
    checker.add_document(invalid_axiom)
    errors = checker.validate_all()
    assert len(errors) == 1
    assert "Invalid cross-reference in Axiom(id=@AXIOM-002): @REQ-002 does not exist" in errors
    assert "Invalid cross-reference in Axiom(id=@AXIOM-002): @REQ-002 does not exist" in caplog.text

    # Test missing links
    invalid_requirement = Requirement({'id': '@REQ-002', 'description': 'Invalid requirement', 'linked_problem_statements': [], 'linked_test_cases': []})
    checker.add_document(invalid_requirement)
    errors = checker.validate_all()
    assert len(errors) == 3
    assert "Validation error in Requirement(id=@REQ-002): Requirement must have at least one linked problem statement" in errors
    assert "Validation error in Requirement(id=@REQ-002): Requirement must have at least one linked test case" in errors
    assert "Invalid cross-reference in Axiom(id=@AXIOM-002): @REQ-002 does not exist" not in errors
    for error in errors:
        assert error in caplog.text

def test_integrity_checker_with_invalid_documents(caplog):
    caplog.set_level(logging.DEBUG)
    
    checker = IntegrityChecker()

    # Create invalid documents
    invalid_axiom = Axiom({'id': '@AXIOM-001', 'description': 'Invalid axiom', 'linked_requirements': []})
    invalid_requirement = Requirement({'id': '@REQ-001', 'description': 'Invalid requirement', 'linked_problem_statements': [], 'linked_test_cases': []})
    invalid_problem_statement = ProblemStatement({'id': '@PROB-001', 'description': 'Invalid problem', 'linked_research_items': [], 'linked_requirements': []})

    checker.add_document(invalid_axiom)
    checker.add_document(invalid_requirement)
    checker.add_document(invalid_problem_statement)

    errors = checker.validate_all()
    assert len(errors) == 5
    assert "Validation error in Axiom(id=@AXIOM-001): Axiom must have at least one linked requirement" in errors
    assert "Validation error in Requirement(id=@REQ-001): Requirement must have at least one linked problem statement" in errors
    assert "Validation error in Requirement(id=@REQ-001): Requirement must have at least one linked test case" in errors
    assert "Validation error in ProblemStatement(id=@PROB-001): Problem Statement must have at least one linked research item" in errors
    assert "Validation error in ProblemStatement(id=@PROB-001): Problem Statement must have at least one linked requirement" in errors
    for error in errors:
        assert error in caplog.text

def test_generate_full_report():
    checker = IntegrityChecker()

    # Create sample documents
    axiom = Axiom({'id': '@AXIOM-001', 'description': 'Test axiom', 'linked_requirements': ['@REQ-001']})
    requirement = Requirement({'id': '@REQ-001', 'description': 'Test requirement', 'linked_problem_statements': ['@PROB-001'], 'linked_test_cases': ['@TEST-001']})
    problem_statement = ProblemStatement({'id': '@PROB-001', 'description': 'Test problem', 'linked_research_items': ['@RES-001'], 'linked_requirements': ['@REQ-001']})

    documents = [axiom, requirement, problem_statement]
    errors = ["Sample error 1", "Sample error 2"]

    full_report = checker.generate_full_report(documents, errors)

    assert "Project Document Summary" in full_report
    assert "Total Documents: 3" in full_report
    assert "Document Type Breakdown:" in full_report
    assert "Axioms: 1" in full_report
    assert "Requirements: 1" in full_report
    assert "ProblemStatements: 1" in full_report
    assert "Document Details:" in full_report
    assert "@AXIOM-001: Test axiom" in full_report
    assert "@REQ-001: Test requirement" in full_report
    assert "@PROB-001: Test problem" in full_report
    assert "Validation Report" in full_report
    assert "Total Errors: 2" in full_report
    assert "Sample error 1" in full_report
    assert "Sample error 2" in full_report
