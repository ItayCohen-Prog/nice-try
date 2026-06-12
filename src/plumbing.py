# Low level, internal API for the library. 
from pathlib import Path


class NtryFilesys:
    def __init__(self, root: Path | None = None):
        if root is None:
            root = Path.cwd()
        self.root = root
        self.ntry_dir = root / ".nice-try"
    
    @classmethod
    def find_project_root(cls, start: Path | None = None) -> Path:
        if start is None:
            start = Path.cwd()

        current = start.resolve()

        for folder in [current, *current.parents]:
            if (folder / ".nice-try").is_dir():
                return folder

        raise FileNotFoundError("Not inside a nice-try project. Run `ntry init` first.")


    def create_empty_filesystem(self) -> Path:

        if self.ntry_dir.exists():
            raise FileExistsError(f"{self.ntry_dir} already exists. Please choose a different directory or remove the existing one.")
        
        self.ntry_dir.mkdir()

        (self.ntry_dir / "objects").mkdir()
        (self.ntry_dir / "objects" / "blobs").mkdir()
        (self.ntry_dir / "objects" / "trees").mkdir()

        (self.ntry_dir / "bases").mkdir()
        (self.ntry_dir / "tries").mkdir()
        
        return self.ntry_dir