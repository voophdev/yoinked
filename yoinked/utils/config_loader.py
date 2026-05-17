import yaml
from pathlib import Path


class ConfigLoader:
    @staticmethod
    def load(path: str) -> dict:
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"Config not found: {path}")

        with open(file_path, "r") as f:
            return yaml.safe_load(f)
