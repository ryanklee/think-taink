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

    def get_linked_requirements(self) -> List[str]:
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
        super().validate()
        if not self.id.startswith('@AXIOM-'):
            self.logger.error(f"Invalid Axiom ID: {self.id}")
            raise ValueError(f"Axiom ID must start with '@AXIOM-': {self.id}")
        if not self.description:
            self.logger.error(f"Axiom {self.id} is missing a description")
            raise ValueError(f"Axiom {self.id} must have a description")
        if not self.linked_requirements:
            self.logger.error(f"Axiom {self.id} has no linked requirements")
            raise ValueError(f"Axiom {self.id} must have at least one linked requirement")
        self.logger.debug(f"Axiom {self.id} passed validation")

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
from .base_document import BaseDocument
from .axiom import Axiom
from typing import List
# Remove circular import

__all__ = ['BaseDocument', 'Axiom', 'Requirement', 'ProblemStatement']
