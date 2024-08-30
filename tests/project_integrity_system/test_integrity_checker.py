import pytest
from src.project_integrity_system import IntegrityChecker, Axiom, Requirement, ProblemStatement

def test_integrity_checker():
    checker = IntegrityChecker()

    # Create valid documents
    axiom = Axiom({'id': '@AXIOM-001', 'description': 'Test axiom', 'linked_requirements': ['@REQ-001']})
    requirement = Requirement({'id': '@REQ-001', 'description': 'Test requirement', 'linked_problem_statements': ['@PROB-001'], 'linked_test_cases': ['@TEST-001']})
    problem_statement = ProblemStatement({'id': '@PROB-001', 'description': 'Test problem', 'linked_research_items': ['@RES-001'], 'linked_requirements': ['@REQ-001']})

    checker.add_document(axiom)
    checker.add_document(requirement)
    checker.add_document(problem_statement)

    # Test valid configuration
    assert checker.validate_all() == []

    # Test invalid cross-reference
    invalid_axiom = Axiom({'id': '@AXIOM-002', 'description': 'Invalid axiom', 'linked_requirements': ['@REQ-002']})
    checker.add_document(invalid_axiom)
    errors = checker.validate_all()
    assert len(errors) == 1
    assert "Invalid cross-reference in @AXIOM-002: @REQ-002 does not exist" in errors[0]

    # Test missing links
    invalid_requirement = Requirement({'id': '@REQ-002', 'description': 'Invalid requirement', 'linked_problem_statements': [], 'linked_test_cases': ['@TEST-002']})
    checker.add_document(invalid_requirement)
    errors = checker.validate_all()
    assert len(errors) == 3
    assert any("must be linked to at least one Problem Statement" in error for error in errors)
    assert any("must have at least one linked problem statement" in error for error in errors)

def test_integrity_checker_with_invalid_documents():
    checker = IntegrityChecker()

    # Create invalid documents
    invalid_axiom = Axiom({'id': '@AXIOM-001', 'description': 'Invalid axiom', 'linked_requirements': []})
    invalid_requirement = Requirement({'id': '@REQ-001', 'description': 'Invalid requirement', 'linked_problem_statements': [], 'linked_test_cases': []})
    invalid_problem_statement = ProblemStatement({'id': '@PROB-001', 'description': 'Invalid problem', 'linked_research_items': [], 'linked_requirements': []})

    checker.add_document(invalid_axiom)
    checker.add_document(invalid_requirement)
    checker.add_document(invalid_problem_statement)

    errors = checker.validate_all()
    assert len(errors) == 6
    assert any("Axiom @AXIOM-001 must be linked to at least one Requirement" in error for error in errors)
    assert any("Requirement @REQ-001 must be linked to at least one Problem Statement" in error for error in errors)
    assert any("Requirement @REQ-001 must have at least one linked test case" in error for error in errors)
    assert any("Problem Statement @PROB-001 must have at least one linked research item" in error for error in errors)
    assert any("Problem Statement @PROB-001 must be linked to at least one Requirement" in error for error in errors)
