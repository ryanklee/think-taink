from abc import ABC, abstractmethod
import yaml

class BaseDocument(ABC):
    def __init__(self, data):
        self.data = data

    @classmethod
    def from_yaml(cls, yaml_string):
        data = yaml.safe_load(yaml_string)
        return cls(data)

    @abstractmethod
    def validate(self):
        pass

    def to_dict(self):
        return self.data
