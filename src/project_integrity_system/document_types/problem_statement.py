from .base_document import BaseDocument
from typing import List

class ProblemStatement(BaseDocument):
    def __init__(self, data):
        super().__init__(data)
        self.description = data.get('description')
        self.linked_research_items = data.get('linked_research_items', [])
        self.linked_requirements = data.get('linked_requirements', [])

    def validate(self):
        super().validate()
        if not self.id.startswith('@PROB-'):
            self.logger.error(f"Invalid Problem Statement ID: {self.id}")
            raise ValueError(f"Problem Statement ID must start with '@PROB-': {self.id}")
        if not self.description:
            self.logger.error(f"Problem Statement {self.id} is missing a description")
            raise ValueError(f"Problem Statement {self.id} must have a description")
        if not self.linked_research_items:
            self.logger.error(f"Problem Statement {self.id} has no linked research items")
            raise ValueError(f"Problem Statement {self.id} must have at least one linked research item")
        if not self.linked_requirements:
            self.logger.error(f"Problem Statement {self.id} has no linked requirements")
            raise ValueError(f"Problem Statement {self.id} must have at least one linked requirement")
        self.logger.debug(f"Problem Statement {self.id} passed validation")

    def get_linked_ids(self) -> List[str]:
        return self.linked_research_items + self.linked_requirements

    def get_document_type(self) -> str:
        return "ProblemStatement"
