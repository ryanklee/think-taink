import pytest
from src.project_integrity_system.document_types.axiom import Axiom

def test_axiom_creation():
    data = {
        'id': '@AXIOM-001',
        'description': 'Test axiom',
        'linked_requirements': ['@REQ-001']
    }
    axiom = Axiom(data)
    assert axiom.id == '@AXIOM-001'
    assert axiom.description == 'Test axiom'
    assert axiom.linked_requirements == ['@REQ-001']

def test_axiom_validation():
    valid_data = {
        'id': '@AXIOM-001',
        'description': 'Test axiom',
        'linked_requirements': ['@REQ-001']
    }
    axiom = Axiom(valid_data)
    axiom.validate()  # Should not raise an exception

    invalid_data = {
        'id': 'INVALID-001',
        'description': 'Test axiom',
        'linked_requirements': []
    }
    invalid_axiom = Axiom(invalid_data)
    with pytest.raises(ValueError):
        invalid_axiom.validate()

def test_axiom_from_yaml():
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
