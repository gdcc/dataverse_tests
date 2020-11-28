from json import dump, load
import os
from pyDataverse.api import NativeApi
from pyDataverse.utils import read_json, write_json


dir_path = os.path.dirname(os.path.realpath(__file__))


def collect_data(base_url: str, api_token: str) -> None:
    api = NativeApi(base_url, api_token)
    resp = api.get_children(children_types=["dataverses", "datasets", "datafiles"])
    write_json(os.path.join(dir_path, "tree.json"), resp)


def generate_data() -> None:
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
