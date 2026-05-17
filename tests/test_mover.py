from pathlib import Path


def test_move_nonexistent(mover: object):
    res = mover.move("no-file.txt", "dest")
    assert res["success"] is False
    assert res["error"] == "source_file_not_found"


def test_move_and_resolve_duplicate(mover: object):
    base = mover.base_path
    src = base / "file.txt"
    src.write_text("source")

    dest_dir = base / "dest"
    dest_dir.mkdir()
    (dest_dir / "file.txt").write_text("existing")

    res = mover.move("file.txt", "dest")

    assert res["success"] is True
    dest_path = Path(res["to"])
    assert dest_path.exists()
    assert (dest_dir / "file.txt").read_text() == "existing"
    assert dest_path.name != "file.txt"
