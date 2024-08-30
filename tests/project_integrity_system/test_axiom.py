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

    with pytest.raises(ValueError):
        Axiom({'id': 'INVALID-001', 'description': 'Test axiom', 'linked_requirements': []}).validate()

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

    with pytest.raises(ValueError):
        Requirement({'id': '@REQ-001', 'description': 'Test requirement', 'linked_problem_statements': []}).validate()

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

    with pytest.raises(ValueError):
        ProblemStatement({'id': '@PROB-001', 'description': 'Test problem', 'linked_research_items': []}).validate()

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
