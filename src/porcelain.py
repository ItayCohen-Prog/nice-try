# Top level, user facing API for the library. 

import typer
import plumbing

app = typer.Typer()

@app.command()
def init():
    plumbing.create_empty_filesystem()
    print("Initialized nice-try project.")