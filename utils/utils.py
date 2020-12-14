import glob
from json import dump, dumps, loads, load
import os
import sys
from time import sleep
from pyDataverse.api import NativeApi
from pyDataverse.utils import read_file, dataverse_tree_walker, read_json, write_json
from pyDataverse.models import Dataverse, Dataset, Datafile
from config import Config


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


def collect_data() -> None:
    api = NativeApi(config.BASE_URL, config.API_TOKEN)
    resp = api.get_children(children_types=["dataverses", "datasets", "datafiles"])
    write_json(os.path.join(INSTANCE_DATA_DIR, config.FILENAME_TREE), resp)


def generate_data() -> None:
    data = read_json(os.path.join(INSTANCE_DATA_DIR, config.FILENAME_TREE))
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


def create_testdata(force: bool, publish_datasets=False, publish_root=False) -> None:
    if config.PRODUCTION and not force:
        print(
            "Create test data on production instance not allowed. Use --force to force it."
        )
        sys.exit()
    lst_pids = []
    api = NativeApi(config.BASE_URL, config.API_TOKEN)

    # Publish :root Dataverse
    if publish_root:
        # TODO: Check via API request, if :root is published or not
        resp = api.publish_dataverse(":root")
        print(resp.json())
        sleep(3)

    # Create Dataverse
    dv_parent_alias = ":root"
    dv = Dataverse()
    dv_filename = os.path.join(ROOT_DIR, "aussda_test-data/data/json/dataverse_1.json")
    dv.from_json(read_file(dv_filename))
    dv_alias = dv.get()["alias"]
    resp = api.create_dataverse(dv_parent_alias, dv.json())
    sleep(3)
    # print(resp.json())
    resp = api.publish_dataverse(dv_alias)
    sleep(3)
    # print(resp.json())

    # Create Dataset
    ds = Dataset()
    ds_filename = os.path.join(ROOT_DIR, "aussda_test-data/data/json/dataset_1.json")
    ds.from_json(read_file(ds_filename))
    resp = api.create_dataset(dv_alias, ds.json())
    sleep(3)
    # print(resp.json())
    pid = resp.json()["data"]["persistentId"]
    lst_pids.append(pid)

    # Publish Dataset
    if publish_datasets:
        for pid in lst_pids:
            resp = api.publish_dataset(pid, release_type="major")
            sleep(3)
            print(resp.json())

    # Upload Datafiles
    json_filenames = []

    for filepath in glob.glob(
        os.path.join(ROOT_DIR, "aussda_test-data/data/json/", "*.json")
    ):
        filename = os.path.basename(filepath)
        file_split = filename.split("_")
        if file_split[0] == "datafile":
            json_filenames.append(filepath)

    for filepath in json_filenames:
        df_dict = read_json(filepath)
        filename = os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(filepath))),
            "files",
            df_dict["filename"],
        )
        df = Datafile()
        df.set(df_dict)
        df.set({"pid": pid})
        resp = api.upload_datafile(pid, filename, df.json())
        if filename[-4:] == ".sav" or filename[-4:] == ".dta":
            sleep(30)
        else:
            sleep(10)
        print(resp.json())

    if publish_datasets:
        resp = api.publish_dataset(pid, release_type="major")
        sleep(3)
        # print(resp.json())


def remove_testdata(force: bool, publish_datasets=False) -> None:
    if config.PRODUCTION and not force:
        print(
            "Remote test data on production instance not allowed. Use --force to force it."
        )
        sys.exit()
    api = NativeApi(config.BASE_URL, config.API_TOKEN)

    # Clean up
    dv_alias = "pyDataverse_testing"
    data = api.get_children(dv_alias, children_types=["dataverses", "datasets"])
    dataverses, datasets, datafiles = dataverse_tree_walker(data)
    dataverses.append({"alias": dv_alias})

    # first the datasets
    if publish_datasets:
        for ds in datasets:
            resp = api.destroy_dataset(ds["pid"])
    else:
        for ds in datasets:
            resp = api.delete_dataset(ds["pid"])

    # last the dataverses
    for dv in dataverses:
        resp = api.delete_dataverse(dv["alias"])
