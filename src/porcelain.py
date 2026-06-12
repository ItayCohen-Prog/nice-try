# Top level, user facing API for the library. 

import typer
from plumbing import NtryFilesys

app = typer.Typer()

@app.command()
def init():
    fs = NtryFilesys()
    
    try:
        ntry_dir = fs.create_empty_filesystem()
    except FileExistsError as error:
        typer.secho(f"Error: {error}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Initialized ntry at {ntry_dir}")