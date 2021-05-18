from typing import List

import typer

from utils import collect_data
from utils import create_testdata
from utils import create_user
from utils import generate_data
from utils import remove_testdata


app = typer.Typer()


@app.command("collect")
def collect_command(
    user_handle: str,
    parent: str = ":root",
    data_types: List[str] = ["dataverses", "datasets", "datafiles"],
    filename: str = "tree.json",
    create_json: bool = True,
) -> None:
    collect_data(user_handle, parent, data_types, filename, create_json)
    typer.echo("Data collected")


@app.command("generate")
def generate_command() -> None:
    generate_data()
    typer.echo("Data generated")


@app.command("create-testdata")
def create_testdata_command(config_file: str, force: bool = False) -> None:
    create_testdata(config_file, force)
    typer.echo("Testdata created")


@app.command("create-user")
def create_user_command(config_file: str, force: bool = False) -> None:
    create_user(config_file, force)
    typer.echo("User created")


@app.command("remove-testdata")
def remove_testdata_command(
    user_handle: str,
    parent: str,
    parent_data_type: str = "dataverse",
    data_types: List[str] = ["dataverses", "datasets"],
    force: bool = False,
) -> None:
    remove_testdata(user_handle, parent, data_types, force, parent_data_type, False)
    typer.echo("Testdata removed")


if __name__ == "__main__":
    app()
