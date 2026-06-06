import typer
from constants import APP_NAME, APP_VERSION
from typing import Annotated
from porcelain import app as porcelain_app


app = typer.Typer()

#returns the version of the app and exits.
def version_callback(value: bool):
    if value:
        print(f"Thank you for using {APP_NAME}\n Version: {APP_VERSION}")
        raise typer.Exit()

@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Show version and exit.",
        ),
    ] = None,
):
    pass
    
app.add_typer(porcelain_app)

if __name__ == "__main__":
    app()