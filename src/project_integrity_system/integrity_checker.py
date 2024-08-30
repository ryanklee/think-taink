import logging
from typing import List, Dict, Set
from .document_types import BaseDocument, Axiom, Requirement, ProblemStatement

class IntegrityChecker:
    def __init__(self):
        self.documents: Dict[str, BaseDocument] = {}
        self.logger = logging.getLogger(__name__)

    def add_document(self, document: BaseDocument):
        self.logger.info(f"Adding document: {document}")
        self.documents[document.id] = document

    def validate_all(self) -> List[str]:
        self.logger.info("Starting validation of all documents")
        errors = []
        errors.extend(self._check_individual_documents())
        errors.extend(self._check_linking_rules())
        errors.extend(self._check_cross_references())
        self.logger.info(f"Validation complete. Found {len(errors)} errors.")
        return sorted(list(set(errors)))  # Remove duplicates and sort for consistent output

    def _check_individual_documents(self) -> List[str]:
        self.logger.info("Checking individual documents")
        errors = []
        for doc in self.documents.values():
            try:
                doc.validate()
                self.logger.debug(f"Document {doc} passed individual validation")
            except ValueError as e:
                error_msg = f"Validation error in {doc}: {str(e)}"
                self.logger.error(error_msg)
                errors.append(error_msg)
        return errors

    def _check_cross_references(self) -> List[str]:
        self.logger.info("Checking cross-references")
        errors = []
        for doc in self.documents.values():
            for linked_id in doc.get_linked_ids():
                if linked_id.startswith('@TEST-') or linked_id.startswith('@RES-'):
                    self.logger.debug(f"Skipping validation for {linked_id} in {doc}")
                    continue  # Skip validation for test cases and research items
                if linked_id not in self.documents:
                    error_msg = f"Invalid cross-reference in {doc}: {linked_id} does not exist"
                    self.logger.error(error_msg)
                    errors.append(error_msg)
                else:
                    self.logger.debug(f"Valid cross-reference in {doc}: {linked_id}")
        return errors

    def _check_linking_rules(self) -> List[str]:
        self.logger.info("Checking linking rules")
        errors = []
        for doc in self.documents.values():
            if isinstance(doc, ProblemStatement):
                self._check_problem_statement_links(doc, errors)
            elif isinstance(doc, Requirement):
                self._check_requirement_links(doc, errors)
            elif isinstance(doc, Axiom):
                self._check_axiom_links(doc, errors)
        return errors

    def _check_problem_statement_links(self, doc: ProblemStatement, errors: List[str]):
        if not any(linked_id.startswith('@REQ-') for linked_id in doc.get_linked_ids()):
            error_msg = f"Validation error in {doc}: Problem Statement must have at least one linked requirement"
            self.logger.error(error_msg)
            errors.append(error_msg)
        if not any(linked_id.startswith('@RES-') for linked_id in doc.get_linked_ids()):
            error_msg = f"Validation error in {doc}: Problem Statement must have at least one linked research item"
            self.logger.error(error_msg)
            errors.append(error_msg)

    def _check_requirement_links(self, doc: Requirement, errors: List[str]):
        if not any(linked_id.startswith('@PROB-') for linked_id in doc.get_linked_ids()):
            error_msg = f"Validation error in {doc}: Requirement must have at least one linked problem statement"
            self.logger.error(error_msg)
            errors.append(error_msg)
        if not any(linked_id.startswith('@TEST-') for linked_id in doc.get_linked_ids()):
            error_msg = f"Validation error in {doc}: Requirement must have at least one linked test case"
            self.logger.error(error_msg)
            errors.append(error_msg)

    def _check_axiom_links(self, doc: Axiom, errors: List[str]):
        if not any(linked_id.startswith('@REQ-') for linked_id in doc.get_linked_ids()):
            error_msg = f"Validation error in {doc}: Axiom must have at least one linked requirement"
            self.logger.error(error_msg)
            errors.append(error_msg)

    def generate_document_summary(self, documents: List[BaseDocument]) -> str:
        summary = "Project Document Summary\n"
        
        # Count the number of documents
        total_documents = len(documents)
        summary += f"Total Documents: {total_documents}\n\n"
        
        # Categorize the documents by type
        document_types = {}
        for doc in documents:
            doc_type = doc.get_document_type()
            if doc_type not in document_types:
                document_types[doc_type] = []
            document_types[doc_type].append(doc)
        
        # Add the document type breakdown to the summary
        summary += "Document Type Breakdown:\n"
        for doc_type, docs in document_types.items():
            summary += f"- {doc_type}s: {len(docs)}\n"
        summary += "\n"
        
        # Add the list of document IDs and descriptions for each type
        summary += "Document Details:\n"
        for doc_type, docs in document_types.items():
            if docs:
                summary += f"{doc_type}s:\n"
                for doc in docs:
                    summary += f"- {doc.id}: {doc.data.get('description', 'No description')}\n"
                summary += "\n"
        
        return summary

    def generate_validation_report(self, errors: List[str]) -> str:
        report = "Validation Report\n"
        report += f"Total Errors: {len(errors)}\n\n"

        if errors:
            report += "Errors:\n"
            for error in errors:
                report += f"- {error}\n"
        else:
            report += "No errors found.\n"

        return report

    def generate_full_report(self, documents: List[BaseDocument], errors: List[str]) -> str:
        document_summary = self.generate_document_summary(documents)
        validation_report = self.generate_validation_report(errors)

        full_report = f"{document_summary}\n{validation_report}"
        return full_report
