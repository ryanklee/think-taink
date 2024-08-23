import json
from datetime import datetime
from typing import Dict, List
from src.utils.exceptions import VersionControlError

class PrincipleVersionControl:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.versions = []
        self.load_versions()

    def load_versions(self):
        try:
            with open(self.file_path, 'r') as f:
                self.versions = json.load(f)
        except FileNotFoundError:
            self.versions = []
        except json.JSONDecodeError as e:
            raise VersionControlError(f"Error decoding version file: {str(e)}")
        
        if not self.versions:
            self.add_version({"default": "Initial principle"}, "Initial version")

    def save_versions(self):
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.versions, f, indent=2)
        except IOError as e:
            raise VersionControlError(f"Error saving versions: {str(e)}")

    def add_version(self, principles: Dict[str, str], comment: str):
        version = {
            "timestamp": datetime.now().isoformat(),
            "principles": principles,
            "comment": comment
        }
        self.versions.append(version)
        self.save_versions()

    def get_version(self, index: int = -1) -> Dict:
        try:
            return self.versions[index]
        except IndexError:
            raise VersionControlError(f"Version index {index} out of range")

    def get_all_versions(self) -> List[Dict]:
        return self.versions

    def revert_to_version(self, index: int) -> Dict[str, str]:
        try:
            version = self.versions[index]
            return version["principles"]
        except IndexError:
            raise VersionControlError(f"Version index {index} out of range")
