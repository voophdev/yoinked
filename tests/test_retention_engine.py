from pathlib import Path
import os
import time


def test_retention_archives_file(tmp_path: Path, retention_engine):
    base = tmp_path
    folder = base / "old"
    folder.mkdir()
    source_file = folder / "old.txt"
    source_file.write_text("content")

    # make file old
    old_time = time.time() - (10 * 86400)
    os.utime(str(source_file), (old_time, old_time))

    rules = {"rule1": {"path": "old", "days": 1}}

    engine = retention_engine(rules, archive_path="Archive")
    engine.run()

    archived = base / "Archive" / "rule1" / "old.txt"
    assert archived.exists()
    assert archived.read_text() == "content"
    assert not source_file.exists()
