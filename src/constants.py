#BASIC APP INFO
APP_NAME = "nice-try"
APP_VERSION = "Pre-release 0.1v"

# Nice Try object types
OBJECT_TYPE_BLOB = "blob"
OBJECT_TYPE_SYMLINK = "syml"
OBJECT_TYPE_TREE = "tree"

OBJECT_TYPE_TO_DIR = {
    OBJECT_TYPE_BLOB: "blobs",
    OBJECT_TYPE_SYMLINK: "symls",
    OBJECT_TYPE_TREE: "trees",
}

DEFAULT_NTRYIGNORE = """# Nice Try ignore file
.nice-try
.git
.venv
__pycache__
*.pyc
"""
