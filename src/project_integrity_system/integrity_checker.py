from typing import List, Dict, Set
from .document_types import BaseDocument, Axiom, Requirement, ProblemStatement

class IntegrityChecker:
    def __init__(self):
        self.documents: Dict[str, BaseDocument] = {}

    def add_document(self, document: BaseDocument):
        self.documents[document.id] = document

    def validate_all(self) -> List[str]:
        errors = []
        errors.extend(self._check_individual_documents())
        errors.extend(self._check_linking_rules())
        errors.extend(self._check_cross_references())
        return sorted(errors)  # Sort the errors for consistent output

    def _check_individual_documents(self) -> List[str]:
        errors = []
        for doc in self.documents.values():
            try:
                doc.validate()
            except ValueError as e:
                errors.append(f"Validation error in {doc.id}: {str(e)}")
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
                if not any(linked_id.startswith('@REQ-') for linked_id in doc.get_linked_ids()):
                    errors.append(f"Validation error in {doc.id}: Problem Statement must have at least one linked requirement")
                if not any(linked_id.startswith('@RES-') for linked_id in doc.get_linked_ids()):
                    errors.append(f"Validation error in {doc.id}: Problem Statement must have at least one linked research item")
            elif isinstance(doc, Requirement):
                if not any(linked_id.startswith('@PROB-') for linked_id in doc.get_linked_ids()):
                    errors.append(f"Validation error in {doc.id}: Requirement must have at least one linked problem statement")
                if not any(linked_id.startswith('@TEST-') for linked_id in doc.get_linked_ids()):
                    errors.append(f"Validation error in {doc.id}: Requirement must have at least one linked test case")
            elif isinstance(doc, Axiom):
                if not any(linked_id.startswith('@REQ-') for linked_id in doc.get_linked_ids()):
                    errors.append(f"Validation error in {doc.id}: Axiom must have at least one linked requirement")
        return errors
                if not any(linked_id.startswith('@REQ-') for linked_id in doc.get_linked_ids()):
                    errors.add(f"Validation error in {doc.id}: Axiom must have at least one linked requirement")
        return errors

    def _check_cross_references(self) -> Set[str]:
        errors = set()
        for doc in self.documents.values():
            for linked_id in doc.get_linked_ids():
                if linked_id.startswith('@TEST-') or linked_id.startswith('@RES-'):
                    continue  # Skip validation for test cases and research items
                if linked_id not in self.documents:
                    errors.add(f"Invalid cross-reference in {doc.id}: {linked_id} does not exist")
        return errors
        return errors

    def _check_individual_documents(self) -> Set[str]:
        errors = set()
        for doc in self.documents.values():
            try:
                doc.validate()
            except ValueError as e:
                errors.add(f"Validation error in {doc.id}: {str(e)}")
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

    def validate_all(self) -> List[str]:
        errors = set()
        errors.update(self._check_linking_rules())
        errors.update(self._check_cross_references())
        return list(errors)
