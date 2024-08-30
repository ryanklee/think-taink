from .base_document import BaseDocument

class Axiom(BaseDocument):
    def __init__(self, data):
        super().__init__(data)
        self.id = data.get('id')
        self.description = data.get('description')
        self.linked_requirements = data.get('linked_requirements', [])

    def validate(self):
        if not self.id or not self.id.startswith('@AXIOM-'):
            raise ValueError("Axiom ID must be present and start with '@AXIOM-'")
        if not self.description:
            raise ValueError("Axiom must have a description")
        if not self.linked_requirements:
            raise ValueError("Axiom must have at least one linked requirement")
