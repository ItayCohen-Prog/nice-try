# Top level, user facing API for the library. 

import typer
from plumbing import NtryFilesys

app = typer.Typer()

@app.command()
def init():
    ntry_dir = NtryFilesys()
    ntry_dir.create_empty_filesystem()

    print("Initialized nice-try project.")