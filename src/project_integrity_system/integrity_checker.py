import logging
from typing import List, Dict
from .document_types.base_document import BaseDocument as Document
from .document_types.axiom import Axiom
from .document_types.requirement import Requirement
from .document_types.problem_statement import ProblemStatement

class IntegrityChecker:
    def __init__(self):
        self.documents: Dict[str, Document] = {}
        self.logger = logging.getLogger(__name__)

    def add_document(self, document: Document):
        self.logger.info(f"Adding document: {document}")
        self.documents[document.id] = document

    def validate_all(self) -> List[str]:
        self.logger.info("Starting validation of all documents")
        errors = []
        errors.extend(self._check_individual_documents())
        errors.extend(self._check_cross_references())
        self.logger.info(f"Validation complete. Found {len(errors)} errors.")
        return sorted(list(set(errors)))  # Remove duplicates and sort for consistent output

    def _check_individual_documents(self) -> List[str]:
        self.logger.info("Checking individual documents")
        errors = []
        for doc in self.documents.values():
            doc_errors = doc.validate()
            if doc_errors:
                errors.extend(doc_errors)
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
                    error_msg = f"Invalid cross-reference in {doc.get_document_type()}(id={doc.id}): {linked_id} does not exist"
                    self.logger.error(error_msg)
                    errors.append(error_msg)
                else:
                    self.logger.debug(f"Valid cross-reference in {doc.get_document_type()}(id={doc.id}): {linked_id}")
        return errors

    def generate_document_summary(self) -> str:
        summary = "Project Document Summary\n"
        
        total_documents = len(self.documents)
        summary += f"Total Documents: {total_documents}\n\n"
        
        document_types = {}
        for doc in self.documents.values():
            doc_type = doc.get_document_type()
            if doc_type not in document_types:
                document_types[doc_type] = []
            document_types[doc_type].append(doc)
        
        summary += "Document Type Breakdown:\n"
        for doc_type, docs in document_types.items():
            summary += f"- {doc_type}s: {len(docs)}\n"
        summary += "\n"
        
        summary += "Document Details:\n"
        for doc_type, docs in document_types.items():
            if docs:
                summary += f"{doc_type}s:\n"
                for doc in docs:
                    summary += f"- {doc.id}: {doc.description}\n"
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

    def generate_full_report(self) -> str:
        document_summary = self.generate_document_summary()
        errors = self.validate_all()
        validation_report = self.generate_validation_report(errors)

        full_report = f"{document_summary}\n{validation_report}"
        return full_report
