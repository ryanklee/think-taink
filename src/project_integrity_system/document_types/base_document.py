from abc import ABC, abstractmethod
import yaml
from typing import List, Dict

class BaseDocument(ABC):
    def __init__(self, data: Dict):
        self.data = data
        self.id = data.get('id')

    @classmethod
    def from_yaml(cls, yaml_string: str):
        data = yaml.safe_load(yaml_string)
        return cls(data)

    @abstractmethod
    def validate(self):
        pass

    def to_dict(self) -> Dict:
        return self.data

    def get_linked_ids(self) -> List[str]:
        return []

    @abstractmethod
    def get_document_type(self) -> str:
        pass
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
