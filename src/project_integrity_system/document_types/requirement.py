from .base_document import BaseDocument
from typing import List

class Requirement(BaseDocument):
    def __init__(self, data):
        super().__init__(data)
        self.description = data.get('description')
        self.linked_problem_statements = data.get('linked_problem_statements', [])
        self.linked_test_cases = data.get('linked_test_cases', [])

    def validate(self):
        super().validate()
        if not self.id.startswith('@REQ-'):
            self.logger.error(f"Invalid Requirement ID: {self.id}")
            raise ValueError(f"Requirement ID must start with '@REQ-': {self.id}")
        if not self.description:
            self.logger.error(f"Requirement {self.id} is missing a description")
            raise ValueError(f"Requirement {self.id} must have a description")
        if not self.linked_problem_statements:
            self.logger.error(f"Requirement {self.id} has no linked problem statements")
            raise ValueError(f"Requirement {self.id} must have at least one linked problem statement")
        if not self.linked_test_cases:
            self.logger.error(f"Requirement {self.id} has no linked test cases")
            raise ValueError(f"Requirement {self.id} must have at least one linked test case")
        self.logger.debug(f"Requirement {self.id} passed validation")

    def get_linked_ids(self) -> List[str]:
        return self.linked_problem_statements + self.linked_test_cases

    def get_document_type(self) -> str:
        return "Requirement"
