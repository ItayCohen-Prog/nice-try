# Low level, internal API for the library. 
from pathlib import Path
import hashing

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

    def store_blob(self,blob_data: bytes) -> str:
        blob_object = hashing.build_stored_object("blob", blob_data)
        blob_hash = hashing.hash_bytes(blob_object)
        blob_path = self.ntry_dir / "objects" / "blobs" / blob_hash 

        if not blob_path.exists():
            with blob_path.open("wb") as f:
                f.write(blob_object)

        return blob_hash
    
    def store_tree(self,tree_data: list[tuple[str, str, str]]) -> str:
        tree_object = hashing.build_tree(tree_data)
        tree_hash = hashing.hash_bytes(tree_object)
        tree_path = self.ntry_dir / "objects" / "trees" / tree_hash 

        if not tree_path.exists():
            with tree_path.open("wb") as f:
                f.write(tree_object)

        return tree_hash

    def get_entries(self) -> list[tuple[str, str, str]]:
        entries = []
        for item in self.root.iterdir():
            if item.is_file():
                mode = "blob"
            elif item.is_dir():
                mode = "tree"
            else:
                continue
            
            name = item.name
            hash = self.store_blob(item.read_bytes())
            entries.append((mode, name, hash))
        return entries

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