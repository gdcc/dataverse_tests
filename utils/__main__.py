import os
import typer
from utils import collect_data, generate_data, create_testdata, remove_testdata
from config import Config


app = typer.Typer()
if os.getenv("ENV_FILE"):
    config = Config(_env_file=os.getenv("ENV_FILE"))
else:
    config = Config()


@app.command("collect")
def collect_command() -> None:
    collect_data()
    typer.echo(f"Data collected")


@app.command("generate")
def generate_command() -> None:
    generate_data()
    typer.echo(f"Data generated")


@app.command("create-testdata")
def create_testdata_command(force: bool = False) -> None:
    create_testdata(force)
    typer.echo(f"Testdata created")


@app.command("remove-testdata")
def remove_testdata_command(force: bool = False) -> None:
    remove_testdata(force)
    typer.echo(f"Testdata removed")


if __name__ == "__main__":
    app()
