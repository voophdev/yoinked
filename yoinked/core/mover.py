from pathlib import Path
import shutil


class Mover:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

    def move(self, file_name: str, destination: str):
        src = self.base_path / file_name
        dst_dir = self.base_path / destination
        dst = dst_dir / file_name

        # 1. Ensure destination folder exists
        dst_dir.mkdir(parents=True, exist_ok=True)

        # 2. Safety check: file exists
        if not src.exists():
            return {
                "success": False,
                "error": "source_file_not_found",
                "from": str(src),
                "to": str(dst),
            }

        # 3. Handle duplicate files
        dst = self._resolve_duplicate(dst)

        # 4. Move file
        try:
            shutil.move(str(src), str(dst))

            return {
                "success": True,
                "from": str(src),
                "to": str(dst),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "from": str(src),
                "to": str(dst),
            }

    def _resolve_duplicate(self, path: Path) -> Path:
        """
        If file already exists, rename it safely.
        """
        if not path.exists():
            return path

        stem = path.stem
        suffix = path.suffix
        parent = path.parent

        counter = 1

        while True:
            new_path = parent / f"{stem} ({counter}){suffix}"
            if not new_path.exists():
                return new_path
            counter += 1
