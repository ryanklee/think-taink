from .base_document import BaseDocument
from typing import List

class ProblemStatement(BaseDocument):
    def __init__(self, data):
        super().__init__(data)
        self.description = data.get('description')
        self.linked_research_items = data.get('linked_research_items', [])
        self.linked_requirements = data.get('linked_requirements', [])

    def validate(self):
        if not self.id or not self.id.startswith('@PROB-'):
            raise ValueError("Problem Statement ID must be present and start with '@PROB-'")
        if not self.description:
            raise ValueError("Problem Statement must have a description")
        if not self.linked_research_items:
            raise ValueError("Problem Statement must have at least one linked research item")
        if not self.linked_requirements:
            raise ValueError("Problem Statement must have at least one linked requirement")

    def get_linked_ids(self) -> List[str]:
        return self.linked_research_items + self.linked_requirements

    def get_document_type(self) -> str:
        return "ProblemStatement"

    def validate(self):
        super().validate()
        if not self.linked_research_items:
            raise ValueError("Problem Statement must have at least one linked research item")
        if not self.linked_requirements:
            raise ValueError("Problem Statement must have at least one linked requirement")
