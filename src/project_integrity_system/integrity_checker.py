from typing import List, Dict
from .document_types import BaseDocument, Axiom, Requirement, ProblemStatement

class IntegrityChecker:
    def __init__(self):
        self.documents: Dict[str, BaseDocument] = {}

    def add_document(self, document: BaseDocument):
        self.documents[document.id] = document

    def validate_all(self) -> List[str]:
        errors = []
        for doc in self.documents.values():
            try:
                doc.validate()
            except ValueError as e:
                errors.append(f"Validation error in {doc.id}: {str(e)}")

        errors.extend(self._check_cross_references())
        errors.extend(self._check_linking_rules())

        return errors

    def _check_cross_references(self) -> List[str]:
        errors = []
        for doc in self.documents.values():
            for linked_id in doc.get_linked_ids():
                if linked_id.startswith('@TEST-') or linked_id.startswith('@RES-'):
                    continue  # Skip validation for test cases and research items
                if linked_id not in self.documents:
                    errors.append(f"Invalid cross-reference in {doc.id}: {linked_id} does not exist")
        return errors

    def _check_linking_rules(self) -> List[str]:
        errors = []
        for doc in self.documents.values():
            if isinstance(doc, ProblemStatement):
                if not any(isinstance(self.documents.get(linked_id), Requirement) for linked_id in doc.get_linked_ids()):
                    errors.append(f"Problem Statement {doc.id} must be linked to at least one Requirement")
            elif isinstance(doc, Requirement):
                if not any(isinstance(self.documents.get(linked_id), ProblemStatement) for linked_id in doc.get_linked_ids()):
                    errors.append(f"Requirement {doc.id} must be linked to at least one Problem Statement")
            elif isinstance(doc, Axiom):
                if not any(isinstance(self.documents.get(linked_id), Requirement) for linked_id in doc.get_linked_ids()):
                    errors.append(f"Axiom {doc.id} must be linked to at least one Requirement")
        return errors
