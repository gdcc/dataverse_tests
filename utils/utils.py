import glob
import os
import sys
from json import dump
from json import dumps
from json import load
from json import loads
from time import sleep
from typing import List

from config import Config
from pyDataverse.api import NativeApi
from pyDataverse.models import Datafile
from pyDataverse.models import Dataset
from pyDataverse.models import Dataverse
from pyDataverse.utils import dataverse_tree_walker
from pyDataverse.utils import read_file
from pyDataverse.utils import read_json
from pyDataverse.utils import write_json


if os.getenv("ENV_FILE"):
    config = Config(_env_file=os.getenv("ENV_FILE"))
else:
    config = Config()

INSTANCE_DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "data/instances", config.INSTANCE,
)
if not os.path.isdir(INSTANCE_DATA_DIR):
    os.makedirs(INSTANCE_DATA_DIR)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def collect_data(
    parent: str = ":root",
    data_types: List[str] = ["dataverses", "datasets", "datafiles"],
    filename: str = "tree.json",
    create_json: bool = False,
) -> None:
    api = NativeApi(config.BASE_URL, config.API_TOKEN)
    tree = api.get_children(parent, children_types=data_types)
    write_json(os.path.join(INSTANCE_DATA_DIR, filename), tree)
    if create_json:
        generate_data(filename)


def generate_data(filename: str = "tree.json") -> None:
    data = read_json(os.path.join(INSTANCE_DATA_DIR, filename))
    dataverses, datasets, datafiles = dataverse_tree_walker(data)
    filename_dv = os.path.join(INSTANCE_DATA_DIR, config.FILENAME_DATAVERSES)
    if os.path.isfile(filename_dv):
        os.remove(filename_dv)
    filename_ds = os.path.join(INSTANCE_DATA_DIR, config.FILENAME_DATASETS)
    if os.path.isfile(filename_ds):
        os.remove(filename_ds)
    filename_df = os.path.join(INSTANCE_DATA_DIR, config.FILENAME_DATAFILES)
    if os.path.isfile(filename_df):
        os.remove(filename_df)
    write_json(filename_dv, dataverses)
    write_json(filename_ds, datasets)
    write_json(filename_df, datafiles)
    metadata = {
        "dataverses": len(dataverses),
        "datasets": len(datasets),
        "datafiles": len(datafiles),
    }
    write_json(os.path.join(INSTANCE_DATA_DIR, config.FILENAME_METADATA), metadata)
    print(f"- Dataverses: {len(dataverses)}")
    print(f"- Datasets: {len(datasets)}")
    print(f"- Datafiles: {len(datafiles)}")


def create_testdata(config_file: str, force: bool) -> None:
    # Init
    if config.PRODUCTION and not force:
        print(
            "Create testdata on a PRODUCTION instance not allowed. Use --force to force it."
        )
        sys.exit()
    pid_idx = []
    api = NativeApi(config.BASE_URL, config.API_TOKEN)
    workflow = read_json(os.path.join(ROOT_DIR, config_file))

    # Dataverses
    for dv_conf in workflow["dataverses"]:
        dv_alias = None
        if "create" in dv_conf:
            if dv_conf["create"]:
                dv = Dataverse()
                dv_filename = os.path.join(ROOT_DIR, dv_conf["filename"])
                dv.from_json(read_file(dv_filename))
                if "update" in dv_conf:
                    for key, val in dv_conf["update"].items():
                        kwargs = {key: val}
                        dv.set(kwargs)
                dv_alias = dv.get()["alias"]
                resp = api.create_dataverse(dv_conf["parent"], dv.json())

        if "publish" in dv_conf:
            if dv_conf["publish"]:
                if not dv_alias and "alias" in dv_conf:
                    dv_alias = dv_conf["alias"]
                resp = api.publish_dataverse(dv_alias)

    # Datasets
    for ds_conf in workflow["datasets"]:
        pid = None
        if "create" in ds_conf:
            if ds_conf["create"]:
                ds = Dataset()
                ds_filename = os.path.join(ROOT_DIR, ds_conf["filename"])
                ds.from_json(read_file(ds_filename))
                if "update" in ds_conf:
                    for key, val in ds_conf["update"].items():
                        kwargs = {key: val}
                        ds.set(kwargs)
                resp = api.create_dataset(dv_alias, ds.json())
                pid = resp.json()["data"]["persistentId"]
                pid_idx.append(pid)

        if "publish" in ds_conf:
            if ds_conf["publish"]:
                if not pid:
                    print("ERROR: PID missing!")
                    sys.exit()
                resp = api.publish_dataset(pid, release_type="major")

    # Datafiles
    for df_conf in workflow["datafiles"]:
        if "create" in df_conf:
            if df_conf["create"]:
                metadata = read_json(df_conf["metadata-filename"])
                df = Datafile()
                df.set(metadata)
                if "update" in df_conf:
                    for key, val in df_conf["update"].items():
                        kwargs = {key: val}
                        df.set(kwargs)
                pid = pid_idx[df_conf["parent"]]
                df.set({"pid": pid})
                filename = df_conf["filename"]
                resp = api.upload_datafile(pid, filename, df.json())
                if filename[-4:] == ".sav" or filename[-4:] == ".dta":
                    sleep(30)
                else:
                    sleep(3)
                if "publish-dataset" in df_conf:
                    if df_conf["publish-dataset"]:
                        resp = api.publish_dataset(pid, release_type="major")


def remove_testdata(
    config_file: str = None,
    parent: str = None,
    data_types: List[str] = ["dataverses", "datasets"],
    ds_published: bool = False,
    force: bool = False,
) -> None:
    if config.PRODUCTION and not force:
        print(
            "Delete testdata on a PRODUCTION instance not allowed. Use --force to force it."
        )
        sys.exit()
    workflow = read_json(os.path.join(ROOT_DIR, config_file))
    if "parent" in workflow:
        parent = workflow["parent"]
    if "data-types" in workflow:
        data_types = workflow["data-types"]
    if "datasets-published" in workflow:
        datasets_published = workflow["datasets-published"]

    api = NativeApi(config.BASE_URL, config.API_TOKEN)

    # Clean up
    data = api.get_children(parent, children_types=data_types)
    dataverses, datasets, datafiles = dataverse_tree_walker(data)
    if "parent-data-type" in workflow:
        dataverses.append({"dataverse_alias": parent})

    for ds in datasets:
        resp = api.destroy_dataset(ds["pid"])

    for dv in dataverses:
        resp = api.delete_dataverse(dv["dataverse_alias"])
