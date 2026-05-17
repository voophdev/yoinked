from yoinked.core.watcher import is_temp_file, YoinkedHandler
from types import SimpleNamespace
from pathlib import Path


import pytest


@pytest.mark.parametrize("name,expected", [
    ("file.crdownload", True),
    ("file.TMP", True),
    ("file.txt", False),
])
def test_is_temp_file(name, expected):
    assert is_temp_file(Path(name)) is expected


def test_handler_calls_callback(tmp_path, handler_callback, monkeypatch):
    calls, cb = handler_callback

    monkeypatch.setattr(
        "yoinked.core.watcher.wait_for_file_ready", lambda *args, **kwargs: True)

    handler = YoinkedHandler(cb)

    event = SimpleNamespace(
        is_directory=False, src_path=str(tmp_path / "a.txt"))
    handler.on_created(event)

    assert calls.get("name") == "a.txt"


def test_handler_ignores_temp_files(tmp_path):
    called = {}

    def cb(name):
        called["name"] = name

    handler = YoinkedHandler(cb)

    event = SimpleNamespace(
        is_directory=False, src_path=str(tmp_path / "a.txt.part"))
    handler.on_created(event)

    assert called.get("name") is None
