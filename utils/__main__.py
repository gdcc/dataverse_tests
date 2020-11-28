import os
import typer
from utils import collect_data, generate_data


app = typer.Typer()
base_url = os.getenv("BASE_URL")
api_token = os.getenv("API_TOKEN")


@app.command("collect")
def collect_command() -> None:
    collect_data(base_url, api_token)
    typer.echo(f"Data collected")


@app.command("generate")
def generate_command() -> None:
    generate_data()
    typer.echo(f"Data generated")


if __name__ == "__main__":
    app()
