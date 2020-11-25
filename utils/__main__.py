from json import dump, load
import os
import typer
from pyDataverse.api import NativeApi


dir_path = os.path.dirname(os.path.realpath(__file__))

app = typer.Typer()
base_url = os.getenv("BASE_URL")
api_token = os.getenv("API_TOKEN")


def read_json(filename, mode="r", encoding="utf-8"):
    """Read in a json file.

    See more about the json module at
    https://docs.python.org/3.5/library/json.html

    Parameters
    ----------
    filename : str
        Filename with full path.
    mode : str
        Read mode of file. Defaults to `w`. See more at
        https://docs.python.org/3.5/library/functions.html#open
    encoding : str
        Character encoding of file. Defaults to 'utf-8'.

    Returns
    -------
    dict
        Data as a json-formatted string.

    """
    assert isinstance(filename, str)
    assert isinstance(mode, str)
    assert isinstance(encoding, str)

    with open(filename, mode, encoding=encoding) as f:
        data = load(f)

    assert isinstance(data, dict) or isinstance(data, list)
    return data


def write_json(filename, data, mode="w", encoding="utf-8"):
    """Write data to a json file.

    Parameters
    ----------
    filename : str
        Filename with full path.
    data : dict
        Data to be written in the JSON file.
    mode : str
        Write mode of file. Defaults to `w`. See more at
        https://docs.python.org/3/library/functions.html#open
    encoding : str
        Character encoding of file. Defaults to 'utf-8'.

    """
    assert isinstance(filename, str)
    assert isinstance(data, dict) or isinstance(data, list)
    assert isinstance(mode, str)
    assert isinstance(encoding, str)

    with open(filename, mode, encoding=encoding) as f:
        dump(data, f, indent=2)


@app.command("collect")
def collect_command():
    collect_data()
    typer.echo(f"Data collected")


@app.command("generate")
def generate_command():
    generate_data()
    typer.echo(f"Data generated")


def collect_data():
    api = NativeApi(base_url, api_token)
    resp = api.get_children(children_types=["dataverses", "datasets", "datafiles"])
    write_json(os.path.join(dir_path, "tree.json"), resp)


def generate_data():
    data = read_json(os.path.join(dir_path, "tree.json"))
    dataverses, datasets, datafiles = tree_walker(data)
    write_json(os.path.join(dir_path, "dataverses.json"), dataverses)
    write_json(os.path.join(dir_path, "datasets.json"), datasets)
    write_json(os.path.join(dir_path, "datafiles.json"), datafiles)
    metadata = {
        "dataverses": len(dataverses),
        "datasets": len(datasets),
        "datafiles": len(datafiles),
    }
    write_json(os.path.join(dir_path, "metadata.json"), metadata)
    print(f"- Dataverses: {len(dataverses)}")
    print(f"- Datasets: {len(datasets)}")
    print(f"- Datafiles: {len(datafiles)}")


def tree_walker(data):
    dataverses = []
    datasets = []
    datafiles = []

    if type(data) == list:
        for elem in data:
            dv, ds, df = tree_walker(elem)
            dataverses += dv
            datasets += ds
            datafiles += df
    elif type(data) == dict:
        if data["type"] == "dataverse":
            dataverses.append(
                {
                    "dataverse_id": data["dataverse_id"],
                    "title": data["title"],
                    "dataverse_alias": data["dataverse_alias"],
                }
            )
        elif data["type"] == "dataset":
            datasets.append(
                {"dataset_id": data["dataset_id"], "pid": data["pid"],}
            )
        elif data["type"] == "datafile":
            datafiles.append(
                {
                    "datafile_id": data["datafile_id"],
                    "filename": data["filename"],
                    "pid": data["pid"],
                }
            )
        if "children" in data:
            if len(data["children"]) > 0:
                dv, ds, df = tree_walker(data["children"])
                dataverses += dv
                datasets += ds
                datafiles += df
    return dataverses, datasets, datafiles


if __name__ == "__main__":
    app()
