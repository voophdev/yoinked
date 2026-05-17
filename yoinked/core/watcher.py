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
    return file_path.suffix.lower() in TEMP_EXTENSIONS


# ----------------------------
# EVENT HANDLER
# ----------------------------

class YoinkedHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # 1. ignore temp files
        if is_temp_file(file_path):
            print(f"[IGNORED TEMP] {file_path.name}")
            return

        # 2. pass to engine
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
