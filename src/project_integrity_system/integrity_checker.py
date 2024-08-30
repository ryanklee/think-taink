import logging
from typing import List, Dict, Optional
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
        errors.extend(self._check_consistency())
        self.logger.info(f"Validation complete. Found {len(errors)} errors.")
        return sorted(list(set(errors)))  # Remove duplicates and sort for consistent output

    def _check_individual_documents(self) -> List[str]:
        self.logger.info("Checking individual documents")
        errors = []
        for doc in self.documents.values():
            doc_errors = doc.validate()
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

    def _check_consistency(self) -> List[str]:
        self.logger.info("Checking document consistency")
        errors = []
        for doc in self.documents.values():
            if isinstance(doc, Requirement):
                errors.extend(self._check_requirement_consistency(doc))
            elif isinstance(doc, ProblemStatement):
                errors.extend(self._check_problem_statement_consistency(doc))
            elif isinstance(doc, Axiom):
                errors.extend(self._check_axiom_consistency(doc))
        return errors

    def _check_requirement_consistency(self, req: Requirement) -> List[str]:
        errors = []
        for prob_id in req.linked_problem_statements:
            prob = self.documents.get(prob_id)
            if prob and req.id not in prob.linked_requirements:
                errors.append(f"Inconsistency: {req.id} links to {prob_id}, but {prob_id} doesn't link back")
        return errors

    def _check_problem_statement_consistency(self, prob: ProblemStatement) -> List[str]:
        errors = []
        for req_id in prob.linked_requirements:
            req = self.documents.get(req_id)
            if req and prob.id not in req.linked_problem_statements:
                errors.append(f"Inconsistency: {prob.id} links to {req_id}, but {req_id} doesn't link back")
        return errors

    def _check_axiom_consistency(self, axiom: Axiom) -> List[str]:
        errors = []
        for req_id in axiom.linked_requirements:
            req = self.documents.get(req_id)
            if not req:
                errors.append(f"Inconsistency: {axiom.id} links to non-existent requirement {req_id}")
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

    def get_document(self, doc_id: str) -> Optional[Document]:
        return self.documents.get(doc_id)
