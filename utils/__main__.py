import os
import typer
from utils import collect_data, generate_data, create_testdata, remove_testdata


app = typer.Typer()


@app.command("collect")
def collect_command() -> None:
    collect_data()
    typer.echo(f"Data collected")


@app.command("generate")
def generate_command() -> None:
    generate_data()
    typer.echo(f"Data generated")


@app.command("create-testdata")
def create_testdata_command() -> None:
    create_testdata()
    typer.echo(f"Testdata created")


@app.command("remove-testdata")
def remove_testdata_command() -> None:
    remove_testdata()
    typer.echo(f"Testdata removed")


if __name__ == "__main__":
    app()
