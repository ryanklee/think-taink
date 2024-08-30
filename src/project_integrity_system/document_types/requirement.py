from .base_document import BaseDocument
from typing import List

class Requirement(BaseDocument):
    def __init__(self, data):
        super().__init__(data)
        self.description = data.get('description')
        self.linked_problem_statements = data.get('linked_problem_statements', [])
        self.linked_test_cases = data.get('linked_test_cases', [])

    def validate(self):
        errors = super().validate()
        if not self.id.startswith('@REQ-'):
            error_msg = f"Invalid Requirement ID: {self.id}"
            self.logger.error(error_msg)
            errors.append(error_msg)
        if not self.description:
            error_msg = f"Requirement {self.id} is missing a description"
            self.logger.error(error_msg)
            errors.append(error_msg)
        if not self.linked_problem_statements:
            error_msg = f"Requirement {self.id} has no linked problem statements"
            self.logger.error(error_msg)
            errors.append(error_msg)
        if not self.linked_test_cases:
            error_msg = f"Requirement {self.id} has no linked test cases"
            self.logger.error(error_msg)
            errors.append(error_msg)
        if not errors:
            self.logger.debug(f"Requirement {self.id} passed validation")
        return errors

    def get_linked_ids(self) -> List[str]:
        return self.linked_problem_statements + self.linked_test_cases

    def get_document_type(self) -> str:
        return "Requirement"
