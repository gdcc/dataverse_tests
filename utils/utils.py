import glob
from json import dump, dumps, loads, load
import os
import sys
from time import sleep
from pyDataverse.api import NativeApi
from pyDataverse.utils import read_file
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
    dataverses, datasets, datafiles = tree_walker(data)
    write_json(os.path.join(INSTANCE_DATA_DIR, config.FILENAME_DATAVERSES), dataverses)
    write_json(os.path.join(INSTANCE_DATA_DIR, config.FILENAME_DATASETS), datasets)
    write_json(os.path.join(INSTANCE_DATA_DIR, config.FILENAME_DATAFILES), datafiles)
    metadata = {
        "dataverses": len(dataverses),
        "datasets": len(datasets),
        "datafiles": len(datafiles),
    }
    write_json(os.path.join(INSTANCE_DATA_DIR, config.FILENAME_METADATA), metadata)
    print(f"- Dataverses: {len(dataverses)}")
    print(f"- Datasets: {len(datasets)}")
    print(f"- Datafiles: {len(datafiles)}")


def tree_walker(data) -> tuple:
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


def create_testdata(force: bool) -> None:
    if config.PRODUCTION and not force:
        print(
            "Create test data on production instance not allowed. Use --force to force it."
        )
        sys.exit()
    lst_pids = []
    api = NativeApi(config.BASE_URL, config.API_TOKEN)

    # Publish :root Dataverse
    if False:
        # TODO: Check via API request, if :root is published or not
        resp = api.get_dataverse(":root")
        print(resp.json())
        # resp = api.publish_dataverse(":root")
        # sleep(3)
        # print(resp.json())

    # Create Dataverse
    dv = Dataverse()
    dv_alias = "science"
    dv_filename = os.path.join(
        ROOT_DIR, "aussda_test-data/data/json/dataverse_1_testing_science.json"
    )
    dv.from_json(read_file(dv_filename), validate=False)
    resp = api.create_dataverse(dv_alias, dv.to_json(validate=False))
    sleep(3)
    # print(resp.json())
    resp = api.publish_dataverse(dv_alias)
    sleep(3)
    # print(resp.json())

    # Create Dataset
    dv_alias = "science"
    ds = Dataset()
    ds_filename = os.path.join(
        ROOT_DIR, "aussda_test-data/data/json/dataset_1_science.json"
    )
    ds.from_json(read_file(ds_filename), validate=False)
    resp = api.create_dataset(dv_alias, ds.to_json(validate=False))
    sleep(3)
    # print(resp.json())
    pid = resp.json()["data"]["persistentId"]
    lst_pids.append(pid)

    # Publish Dataset
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
        resp = api.upload_datafile(pid, filename, df.to_json(validate=False))
        if filename[-4:] == ".sav" or filename[-4:] == ".dta":
            sleep(30)
        else:
            sleep(10)
        print(resp.json())

    resp = api.publish_dataset(pid, release_type="major")
    sleep(3)
    # print(resp.json())


def remove_testdata(force: bool) -> None:
    if config.PRODUCTION and not force:
        print(
            "Remote test data on production instance not allowed. Use --force to force it."
        )
        sys.exit()
    api = NativeApi(config.BASE_URL, config.API_TOKEN)

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


def read_json(filename: str, mode: str = "r", encoding: str = "utf-8") -> dict:
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
    with open(filename, mode, encoding=encoding) as f:
        data = load(f)

    return data


def write_json(
    filename: str, data: dict, mode: str = "w", encoding: str = "utf-8"
) -> None:
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

    with open(filename, mode, encoding=encoding) as f:
        dump(data, f, indent=2)
