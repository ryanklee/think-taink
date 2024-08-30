from .base_document import BaseDocument
from typing import List

class Axiom(BaseDocument):
    def __init__(self, data):
        super().__init__(data)
        self.description = data.get('description')
        self.linked_requirements = data.get('linked_requirements', [])

    def validate(self):
        errors = super().validate()
        if not self.id.startswith('@AXIOM-'):
            error_msg = f"Invalid Axiom ID: {self.id}"
            self.logger.error(error_msg)
            errors.append(error_msg)
        if not self.description:
            error_msg = f"Axiom {self.id} is missing a description"
            self.logger.error(error_msg)
            errors.append(error_msg)
        if not self.linked_requirements:
            error_msg = f"Axiom {self.id} has no linked requirements"
            self.logger.error(error_msg)
            errors.append(error_msg)
        if not errors:
            self.logger.debug(f"Axiom {self.id} passed validation")
        return errors

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
        errors = super().validate()
        if not self.id.startswith('@AXIOM-'):
            error_msg = f"Invalid Axiom ID: {self.id}"
            self.logger.error(error_msg)
            errors.append(error_msg)
        if not self.description:
            error_msg = f"Axiom {self.id} is missing a description"
            self.logger.error(error_msg)
            errors.append(error_msg)
        if not self.linked_requirements:
            error_msg = f"Axiom {self.id} has no linked requirements"
            self.logger.error(error_msg)
            errors.append(error_msg)
        if not errors:
            self.logger.debug(f"Axiom {self.id} passed validation")
        return errors

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
        errors = super().validate()
        if not self.id.startswith('@AXIOM-'):
            error_msg = f"Invalid Axiom ID: {self.id}"
            self.logger.error(error_msg)
            errors.append(error_msg)
        if not self.description:
            error_msg = f"Axiom {self.id} is missing a description"
            self.logger.error(error_msg)
            errors.append(error_msg)
        if not self.linked_requirements:
            error_msg = f"Axiom {self.id} has no linked requirements"
            self.logger.error(error_msg)
            errors.append(error_msg)
        if not errors:
            self.logger.debug(f"Axiom {self.id} passed validation")
        return errors

    def get_linked_ids(self) -> List[str]:
        return self.linked_requirements

    def get_document_type(self) -> str:
        return "Axiom"
from .base_document import BaseDocument
from .axiom import Axiom
from typing import List
# Remove circular import

__all__ = ['BaseDocument', 'Axiom', 'Requirement', 'ProblemStatement']
