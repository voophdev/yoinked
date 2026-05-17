from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import time


# ----------------------------
# TEMP FILE HANDLING
# ----------------------------

TEMP_EXTENSIONS = {
    ".crdownload",
    ".part",
    ".tmp",
    ".download"
}


def is_temp_file(file_path: Path) -> bool:
    name = file_path.name.lower()

    if name.startswith("unconfirmed"):
        return True

    if file_path.suffix.lower() in TEMP_EXTENSIONS:
        return True

    return False


def wait_for_file_ready(file_path: Path, timeout=30, interval=0.5):
    last_size = -1
    stable = 0

    for _ in range(int(timeout / interval)):
        if not file_path.exists():
            return False

        try:
            size = file_path.stat().st_size
        except Exception:
            time.sleep(interval)
            continue

        if size == last_size:
            stable += 1
        else:
            stable = 0
            last_size = size

        if stable >= 3:
            return True

        time.sleep(interval)

    return False


# ----------------------------
# EVENT HANDLER
# ----------------------------

class YoinkedHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_created(self, event):
        file_path = Path(event.src_path)

        if is_temp_file(file_path):
            return

        if not wait_for_file_ready(file_path):
            return

        self.callback(file_path.name)


# ----------------------------
# WATCHER CORE
# ----------------------------

class Watcher:

    def __init__(self, path_to_watch: str, callback):
        self.path_to_watch = Path(path_to_watch)
        self.callback = callback
        self.observer = Observer()

    def run(self):
        event_handler = YoinkedHandler(self.callback)

        self.observer.schedule(
            event_handler,
            str(self.path_to_watch),
            recursive=False
        )

        self.observer.start()

        print(f"[WATCHER] Watching: {self.path_to_watch}")

        try:
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            print("[WATCHER STOPPED]")
            self.observer.stop()

        self.observer.join()
