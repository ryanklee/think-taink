from typing import Dict
from src.utils.version_control import VersionControl

class EthicalGuidelines:
    def __init__(self, version_control_file: str):
        self.version_control = VersionControl(version_control_file)
        self.guidelines = self.version_control.get_version(0)["data"]
        self.guideline_scores = {
            guideline_name: 1.0 for guideline_name in self.guidelines
        }
