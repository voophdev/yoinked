import os
import queue
import threading

from yoinked.core.watcher import Watcher
from yoinked.core.mover import Mover
from yoinked.core.logger import Logger
from yoinked.rules.router import Router
from yoinked.core.engine import Engine
from yoinked.core.state import FileState
from yoinked.core.retention_engine import RetentionEngine, RetentionWorker
from yoinked.utils.config_loader import ConfigLoader


def main():
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

    rules_config = ConfigLoader.load("config/rules.yml")["rules"]
    router = Router(rules_config)
    mover = Mover(downloads_path)
    logger = Logger("logs/audit.jsonl")
    engine = Engine(router, mover, logger)

    state = FileState()

    file_queue = queue.Queue()

    # worker
    def worker():
        while True:
            file_name = file_queue.get()
            try:
                engine.process_file(file_name)
            finally:
                state.mark_done(file_name)
                file_queue.task_done()

    threading.Thread(target=worker, daemon=True).start()

    retention_config = ConfigLoader.load("config/retention.yml")

    interval_seconds = retention_config.get("interval_seconds", 3600)
    retention_rules = retention_config["retention"]

    retention_engine = RetentionEngine(
        rules=retention_rules,
        base_path=downloads_path,
        logger=logger
    )

    retention_worker = RetentionWorker(
        retention_engine=retention_engine,
        interval_seconds=interval_seconds
    )
    retention_worker.start()

    # watcher callback
    def on_file(file_name: str):
        if state.should_process(file_name):
            file_queue.put(file_name)
        else:
            print(f"[SKIP] {file_name}")

    watcher = Watcher(downloads_path, callback=on_file)

    print(f"[WATCHTOWER STARTED] {downloads_path}")
    watcher.run()


if __name__ == "__main__":
    main()
