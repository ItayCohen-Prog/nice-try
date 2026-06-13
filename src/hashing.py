import hashlib


def hash_bytes(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def build_stored_object(object_type: str, content: bytes) -> bytes:
    header = f"{object_type} {len(content)}\0".encode()
    store_data = header + content
    return store_data


def tree_sort_key(entry: tuple[str, str, str]) -> bytes:
    _kind, name, _object_hash = entry
    return name.encode()


def build_tree_content(entries: list[tuple[str, str, str]]) -> bytes:
    tree_content = b""

    for kind, name, object_hash in sorted(entries, key=tree_sort_key):
        # A Nice Try tree entry is:
        #   kind + space + name + null byte + the raw 20-byte object hash
        entry = f"{kind} {name}\0".encode() + bytes.fromhex(object_hash)
        tree_content += entry

    return tree_content
