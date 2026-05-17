import threading
import time


class FileState:
    def __init__(self, debounce_seconds=2):
        self.processing = set()
        self.last_seen = {}
        self.debounce_seconds = debounce_seconds
        self.lock = threading.Lock()

    def should_process(self, file_name: str) -> bool:
        now = time.time()

        with self.lock:
            # debounce check
            if file_name in self.last_seen:
                if now - self.last_seen[file_name] < self.debounce_seconds:
                    return False

            self.last_seen[file_name] = now

            # duplicate processing check
            if file_name in self.processing:
                return False

            self.processing.add(file_name)
            return True

    def mark_done(self, file_name: str):
        with self.lock:
            self.processing.discard(file_name)
