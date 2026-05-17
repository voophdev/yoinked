from pathlib import Path
from yoinked.models.file_event import FileEvent


class Logger:
    def __init__(self, log_file: str):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(self, event: dict):
        validated = FileEvent(**event)

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(validated.model_dump_json() + "\n")
