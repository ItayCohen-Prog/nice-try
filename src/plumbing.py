import fnmatch
import json
import os
from datetime import datetime
from pathlib import Path

import hashing
from constants import (
    DEFAULT_NTRYIGNORE,
    OBJECT_TYPE_BLOB,
    OBJECT_TYPE_SYMLINK,
    OBJECT_TYPE_TO_DIR,
    OBJECT_TYPE_TREE,
)


class NtryLayoutError(Exception):
    pass


class NtryFilesys:
    def __init__(self, root: Path | None = None):
        if root is None:
            root = Path.cwd()
        self.root = root
        self.ntry_dir = root / ".nice-try"
        self.ignore_list = self.load_ntryignore()

    def parse_ntryignore(self, content: str) -> list[str]:
        return [
            line.strip()
            for line in content.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]

    def load_ntryignore(self) -> list[str]:
        ignore_path = self.root / ".ntryignore"

        if ignore_path.exists():
            content = ignore_path.read_text(encoding="utf-8")
        else:
            content = DEFAULT_NTRYIGNORE

        return self.parse_ntryignore(content)

    def create_default_ntryignore(self) -> None:
        ignore_path = self.root / ".ntryignore"

        if not ignore_path.exists():
            ignore_path.write_text(DEFAULT_NTRYIGNORE, encoding="utf-8")

        self.ignore_list = self.load_ntryignore()

    def is_ignored(self, path: Path) -> bool:
        relative_path = path.relative_to(self.root).as_posix()

        for pattern in self.ignore_list:
            clean_pattern = pattern.rstrip("/")

            if fnmatch.fnmatch(path.name, clean_pattern):
                return True

            if fnmatch.fnmatch(relative_path, clean_pattern):
                return True

        return False

    @classmethod
    def find_project_root(cls, start: Path | None = None) -> Path:
        if start is None:
            start = Path.cwd()

        current = start.resolve()

        for folder in [current, *current.parents]:
            if (folder / ".nice-try").is_dir():
                return folder

        raise FileNotFoundError("Not inside a nice-try project. Run `ntry init` first.")

    def store_object(self, object_type: str, content: bytes) -> str:
        stored_object = hashing.build_stored_object(object_type, content)
        object_hash = hashing.hash_bytes(stored_object)
        object_dir = self.ntry_dir / "objects" / OBJECT_TYPE_TO_DIR[object_type]

        if not object_dir.is_dir():
            raise NtryLayoutError(
                f"Missing nice-try object directory: {object_dir}. Run `ntry init` first."
            )

        object_path = object_dir / object_hash

        if not object_path.exists():
            with object_path.open("wb") as f:
                f.write(stored_object)

        return object_hash

    def write_tree_from_directory(self, directory: Path | None = None) -> str:
        """Store a Nice Try tree for a directory and return its hash.

        This uses a "post-order" walk: each child file or directory is stored
        first, then the parent tree stores the child hashes. That mirrors a
        content-addressed design: parent objects point to child object hashes.
        """
        if directory is None:
            directory = self.root

        entries: list[tuple[str, str, str]] = []

        for item in directory.iterdir():
            if self.is_ignored(item):
                continue

            if item.is_symlink():
                # Store the link target text as the symlink object's content.
                kind = OBJECT_TYPE_SYMLINK
                object_hash = self.store_object(kind, os.readlink(item).encode())
            elif item.is_file():
                kind = OBJECT_TYPE_BLOB
                object_hash = self.store_object(kind, item.read_bytes())
            elif item.is_dir():
                # A directory becomes a tree object, and this parent stores its hash.
                kind = OBJECT_TYPE_TREE
                object_hash = self.write_tree_from_directory(item)
            else:
                continue

            entries.append((kind, item.name, object_hash))

        return self.store_object(OBJECT_TYPE_TREE, hashing.build_tree_content(entries))

    def store_base(self, root_hash: str) -> Path:
        now = datetime.now().astimezone()
        milliseconds = now.microsecond // 1000
        timestamp = f"{now.strftime('%m/%d/%y')} {now.strftime('%H:%M:%S')}.{milliseconds:03d}"
        base_data = {
            "root_tree_hash": root_hash,
            "date": timestamp,
        }

        base_dir = self.ntry_dir / "bases"
        if not base_dir.is_dir():
            raise NtryLayoutError(
                f"Missing nice-try bases directory: {base_dir}. Run `ntry init` first."
            )

        filename_stem = f"{now.strftime('%Y%m%d%H%M%S')}{milliseconds:03d}"
        filename_width = len(filename_stem)
        filename_number = int(filename_stem)

        while True:
            base_path = base_dir / f"{filename_number:0{filename_width}d}.json"

            try:
                with base_path.open("x", encoding="utf-8") as f:
                    json.dump(base_data, f, indent=2, ensure_ascii=False)
                    f.write("\n")
            except FileExistsError:
                filename_number += 1
            else:
                return base_path

    def create_empty_filesystem(self) -> Path:

        if self.ntry_dir.exists():
            raise FileExistsError(f"{self.ntry_dir} already exists. Please choose a different directory or remove the existing one.")

        self.ntry_dir.mkdir()

        (self.ntry_dir / "objects").mkdir()
        for object_dir in dict.fromkeys(OBJECT_TYPE_TO_DIR.values()):
            (self.ntry_dir / "objects" / object_dir).mkdir()

        (self.ntry_dir / "bases").mkdir()
        (self.ntry_dir / "tries").mkdir()
        self.create_default_ntryignore()

        return self.ntry_dir
