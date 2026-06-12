#does all that is related to the process of hashing files, and folder trees.
import hashlib
from pathlib import Path

import hashlib


def hash_bytes(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()

def build_stored_object(object_type: str, content: bytes) -> bytes:
    header = f"{object_type} {len(content)}\0".encode()
    store_data = header + content
    return store_data

def build_tree(entries: list[tuple[str, str, str]]) -> bytes:
    tree_content = b""
    for mode, name, hash in entries:
        entry = f"{mode} {name}\0".encode() + bytes.fromhex(hash)
        tree_content += entry

    return build_stored_object("tree", tree_content)