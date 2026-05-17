import json
from pathlib import Path


def test_logger_writes_jsonl(logger: object):
    log_path: Path = logger.log_file

    event = {
        "type": "sort",
        "action": "log",
        "file": "a.txt",
        "source": "src",
        "destination": "dst",
        "status": True,
        "rule": "r",
        "match": "m",
    }

    logger.log(event)

    content = log_path.read_text(encoding="utf-8").strip()
    assert content

    record = json.loads(content.splitlines()[-1])
    assert record["type"] == "sort"
    assert record["file"] == "a.txt"
