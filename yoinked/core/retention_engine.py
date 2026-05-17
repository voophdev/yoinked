import threading
import time
import shutil

from pathlib import Path


class RetentionEngine:
    def __init__(self, rules: dict, base_path: str, logger=None, archive_path="Archive/"):
        self.rules = rules
        self.base_path = Path(base_path)
        self.archive_path = self.base_path / archive_path
        self.logger = logger

    def run(self):
        now = time.time()

        for rule_name, rule in self.rules.items():
            folder = self.base_path / rule["path"]
            days = rule["days"]

            if not folder.exists():
                continue

            for file in folder.rglob("*"):
                if not file.is_file():
                    continue

                age_days = (now - file.stat().st_mtime) / 86400

                if age_days >= days:
                    self._archive(file, rule_name)

    def _archive(self, file: Path, rule_name: str):
        source = str(file)

        target_dir = self.archive_path / rule_name
        target_dir.mkdir(parents=True, exist_ok=True)

        target = target_dir / file.name

        shutil.move(str(file), str(target))

        if self.logger:
            self.logger.log({
                "type": "retention",
                "action": "archive",
                "file": file.name,
                "source": source,
                "destination": str(target),
                "rule": rule_name,
                "match": "age",
                "status": True
            })

        print(f"[ARCHIVE] {file} → {target}")


class RetentionWorker:
    def __init__(self, retention_engine: RetentionEngine, interval_seconds: int):
        self.retention_engine = retention_engine
        self.interval_seconds = interval_seconds
        self._stop = threading.Event()

    def start(self):
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()
        return thread

    def _run(self):
        print("[RETENTION] started")

        while not self._stop.is_set():
            try:
                self.retention_engine.run()
            except Exception as e:
                print(f"[RETENTION ERROR] {e}")

            self._stop.wait(self.interval_seconds)

    def stop(self):
        self._stop.set()
