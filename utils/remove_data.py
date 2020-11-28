import os
from time import sleep
from utils import tree_walker

from pyDataverse.api import NativeApi
from pyDataverse.utils import read_csv_as_dicts, read_file
from pyDataverse.models import Dataverse, Dataset, Datafile


ROOT_DIR = dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


if __name__ == "__main__":
    print("START --------------------------")

    INSTANCE = os.getenv("INSTANCE")
    BASE_URL = os.getenv("BASE_URL")
    API_TOKEN = os.getenv("API_TOKEN")
    api = NativeApi(BASE_URL, API_TOKEN)

    # Clean up
    data = api.get_children("science", children_types=["dataverses", "datasets"])
    dataverses, datasets, datafiles = tree_walker(data)
    dataverses.append({"alias": "science"})

    # first the datasets
    for ds in datasets:
        resp = api.destroy_dataset(ds["pid"])
        print(resp.json())

    # last the dataverses
    for dv in dataverses:
        resp = api.delete_dataverse(dv["alias"])
        print(resp.json())

    print("END --------------------------")
