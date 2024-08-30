from .base_document import BaseDocument
from typing import List

class ProblemStatement(BaseDocument):
    def __init__(self, data):
        super().__init__(data)
        self.description = data.get('description')
        self.linked_research_items = data.get('linked_research_items', [])
        self.linked_requirements = data.get('linked_requirements', [])

    def validate(self):
        errors = super().validate()
        if not self.id.startswith('@PROB-'):
            error_msg = f"Invalid Problem Statement ID: {self.id}"
            self.logger.error(error_msg)
            errors.append(error_msg)
        if not self.description:
            error_msg = f"Problem Statement {self.id} is missing a description"
            self.logger.error(error_msg)
            errors.append(error_msg)
        if not self.linked_research_items:
            error_msg = f"Problem Statement {self.id} has no linked research items"
            self.logger.error(error_msg)
            errors.append(error_msg)
        if not self.linked_requirements:
            error_msg = f"Problem Statement {self.id} has no linked requirements"
            self.logger.error(error_msg)
            errors.append(error_msg)
        if not errors:
            self.logger.debug(f"Problem Statement {self.id} passed validation")
        return errors

    def get_linked_ids(self) -> List[str]:
        return self.linked_research_items + self.linked_requirements

    def get_document_type(self) -> str:
        return "ProblemStatement"
