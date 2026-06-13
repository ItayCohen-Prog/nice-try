# Top level, user facing API for the library. 

import typer
from plumbing import NtryFilesys, NtryLayoutError

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

@app.command()
def base():
    try:
        project_root = NtryFilesys.find_project_root()
        fs = NtryFilesys(project_root)
    except FileNotFoundError as error:
        typer.secho(f"Error: {error}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    try:
        root_tree_hash = fs.write_tree_from_directory()
        fs.store_base(root_tree_hash)
    except NtryLayoutError as error:
        typer.secho(f"Error: {error}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
