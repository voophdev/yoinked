import time
from yoinked.core.state import FileState


def test_debounce_and_processing(file_state):
    fs = file_state

    assert fs.should_process("a.txt") is True
    assert fs.should_process("a.txt") is False

    fs.mark_done("a.txt")
    time.sleep(fs.debounce_seconds + 0.01)

    assert fs.should_process("a.txt") is True
    fs.mark_done("a.txt")
