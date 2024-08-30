from project_integrity_system.document_types.base_document import BaseDocument
from project_integrity_system.document_types.requirement import Requirement
from typing import List

class Axiom(BaseDocument):
    def __init__(self, data):
        super().__init__(data)
        self.description = data.get('description')
        self.linked_requirements = data.get('linked_requirements', [])

    def validate(self):
        if not self.id or not self.id.startswith('@AXIOM-'):
            raise ValueError("Axiom ID must be present and start with '@AXIOM-'")
        if not self.description:
            raise ValueError("Axiom must have a description")
        if not self.linked_requirements:
            raise ValueError("Axiom must have at least one linked requirement")

    def get_linked_ids(self) -> List[str]:
        return self.linked_requirements

    def get_document_type(self) -> str:
        return "Axiom"
from .base_document import BaseDocument
from .axiom import Axiom
from .requirement import Requirement
from .problem_statement import ProblemStatement

__all__ = ['BaseDocument', 'Axiom', 'Requirement', 'ProblemStatement']
from .base_document import BaseDocument
from typing import List

class Axiom(BaseDocument):
    def __init__(self, data):
        super().__init__(data)
        self.description = data.get('description')
        self.linked_requirements = data.get('linked_requirements', [])

    def validate(self):
        if not self.id or not self.id.startswith('@AXIOM-'):
            raise ValueError("Axiom ID must be present and start with '@AXIOM-'")
        if not self.description:
            raise ValueError("Axiom must have a description")
        if not self.linked_requirements:
            raise ValueError("Axiom must have at least one linked requirement")

    def get_linked_ids(self) -> List[str]:
        return self.linked_requirements

    def get_document_type(self) -> str:
        return "Axiom"
from .base_document import BaseDocument
from typing import List

class Axiom(BaseDocument):
    def __init__(self, data):
        super().__init__(data)
        self.description = data.get('description')
        self.linked_requirements = data.get('linked_requirements', [])

    def validate(self):
        if not self.id or not self.id.startswith('@AXIOM-'):
            raise ValueError("Axiom ID must be present and start with '@AXIOM-'")
        if not self.description:
            raise ValueError("Axiom must have a description")
        if not self.linked_requirements:
            raise ValueError("Axiom must have at least one linked requirement")

    def get_linked_ids(self) -> List[str]:
        return self.linked_requirements

    def get_document_type(self) -> str:
        return "Axiom"
