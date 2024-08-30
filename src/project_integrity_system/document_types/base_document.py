from abc import ABC, abstractmethod
import yaml
from typing import List, Dict
import logging

class BaseDocument(ABC):
    def __init__(self, data: Dict):
        self.data = data
        self.id = data.get('id')
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @classmethod
    def from_yaml(cls, yaml_string: str):
        try:
            data = yaml.safe_load(yaml_string)
            return cls(data)
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML: {e}")
            raise ValueError(f"Invalid YAML format: {e}")

    def validate(self):
        errors = []
        if not self.id:
            error_msg = f"{self.get_document_type()} is missing an ID"
            self.logger.error(error_msg)
            errors.append(error_msg)
        return errors

    def to_dict(self) -> Dict:
        return self.data

    @abstractmethod
    def get_linked_ids(self) -> List[str]:
        pass

    @abstractmethod
    def get_document_type(self) -> str:
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
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
from abc import ABC, abstractmethod
from typing import List, Dict

class Document(ABC):
    def __init__(self, id: str, description: str):
        self.id = id
        self.description = description

    @abstractmethod
    def validate(self) -> List[str]:
        pass

    @abstractmethod
    def get_linked_ids(self) -> List[str]:
        pass

    @abstractmethod
    def get_document_type(self) -> str:
        pass

class Axiom(Document):
    def __init__(self, id: str, description: str, linked_requirements: List[str]):
        super().__init__(id, description)
        self.linked_requirements = linked_requirements

    def validate(self) -> List[str]:
        errors = []
        if not self.id.startswith('@AXIOM-'):
            errors.append(f"Axiom ID must start with '@AXIOM-': {self.id}")
        if not self.description:
            errors.append(f"Axiom {self.id} must have a description")
        if not self.linked_requirements:
            errors.append(f"Axiom {self.id} must have at least one linked requirement")
        return errors

    def get_linked_ids(self) -> List[str]:
        return self.linked_requirements

    def get_document_type(self) -> str:
        return "Axiom"

class Requirement(Document):
    def __init__(self, id: str, description: str, linked_problem_statements: List[str], linked_test_cases: List[str]):
        super().__init__(id, description)
        self.linked_problem_statements = linked_problem_statements
        self.linked_test_cases = linked_test_cases

    def validate(self) -> List[str]:
        errors = []
        if not self.id.startswith('@REQ-'):
            errors.append(f"Requirement ID must start with '@REQ-': {self.id}")
        if not self.description:
            errors.append(f"Requirement {self.id} must have a description")
        if not self.linked_problem_statements:
            errors.append(f"Requirement {self.id} must have at least one linked problem statement")
        if not self.linked_test_cases:
            errors.append(f"Requirement {self.id} must have at least one linked test case")
        return errors

    def get_linked_ids(self) -> List[str]:
        return self.linked_problem_statements + self.linked_test_cases

    def get_document_type(self) -> str:
        return "Requirement"

class ProblemStatement(Document):
    def __init__(self, id: str, description: str, linked_research_items: List[str], linked_requirements: List[str]):
        super().__init__(id, description)
        self.linked_research_items = linked_research_items
        self.linked_requirements = linked_requirements

    def validate(self) -> List[str]:
        errors = []
        if not self.id.startswith('@PROB-'):
            errors.append(f"Problem Statement ID must start with '@PROB-': {self.id}")
        if not self.description:
            errors.append(f"Problem Statement {self.id} must have a description")
        if not self.linked_research_items:
            errors.append(f"Problem Statement {self.id} must have at least one linked research item")
        if not self.linked_requirements:
            errors.append(f"Problem Statement {self.id} must have at least one linked requirement")
        return errors

    def get_linked_ids(self) -> List[str]:
        return self.linked_research_items + self.linked_requirements

    def get_document_type(self) -> str:
        return "ProblemStatement"
