import sys
from pathlib import Path
import pytest

# Ensure project root is on sys.path so tests can import the `yoinked` package
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


@pytest.fixture
def mover(tmp_path: Path):
    from yoinked.core.mover import Mover
    return Mover(str(tmp_path))


@pytest.fixture
def logger(tmp_path: Path):
    from yoinked.core.logger import Logger
    log_file = tmp_path / "logs" / "audit.jsonl"
    return Logger(str(log_file))


@pytest.fixture
def file_state():
    from yoinked.core.state import FileState
    return FileState(debounce_seconds=0.01)


@pytest.fixture
def retention_engine(tmp_path: Path):
    from yoinked.core.retention_engine import RetentionEngine

    def _make(rules, archive_path="Archive"):
        return RetentionEngine(rules, str(tmp_path), logger=None, archive_path=archive_path)

    return _make


@pytest.fixture
def handler_callback():
    calls = {}

    def cb(name):
        calls["name"] = name

    return calls, cb
