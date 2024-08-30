from .base_document import BaseDocument
from typing import List

class Requirement(BaseDocument):
    def __init__(self, data):
        super().__init__(data)
        self.description = data.get('description')
        self.linked_problem_statements = data.get('linked_problem_statements', [])
        self.linked_test_cases = data.get('linked_test_cases', [])

    def validate(self):
        if not self.id or not self.id.startswith('@REQ-'):
            raise ValueError("Requirement ID must be present and start with '@REQ-'")
        if not self.description:
            raise ValueError("Requirement must have a description")
        if not self.linked_problem_statements:
            raise ValueError("Requirement must have at least one linked problem statement")
        if not self.linked_test_cases:
            raise ValueError("Requirement must have at least one linked test case")

    def get_linked_ids(self) -> List[str]:
        return self.linked_problem_statements + self.linked_test_cases

    def get_document_type(self) -> str:
        return "Requirement"
