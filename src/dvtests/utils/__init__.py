import os
import sys
from time import sleep
from typing import List

import requests
from pyDataverse.api import NativeApi
from pyDataverse.models import Datafile
from pyDataverse.models import Dataset
from pyDataverse.models import Dataverse
from pyDataverse.utils import dataverse_tree_walker
from pyDataverse.utils import read_file
from pyDataverse.utils import read_json
from pyDataverse.utils import write_json

from dvtests.settings import UtilsSettings


if os.getenv("ENV_FILE"):
    config = UtilsSettings(_env_file=os.getenv("ENV_FILE"))
else:
    config = UtilsSettings()

ROOT_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)
UTILS_DATA_DIR = os.path.join(ROOT_DIR, "data/utils", config.INSTANCE,)


def collect_data(
    user_handle: str,
    parent: str,
    data_types: List[str],
    filename: str,
    create_json: bool,
) -> None:
    """Collect data of a Dataverse installation.

    Collect data from a data node down the Dataverse
    tree-like data structure.

    Collects the complete data of a Dataverse instance in
    a tree structure (`tree.json`), containing all
    Dataverses, Datasets and Datafiles. The file is
    stored in your instance directory (e. g.
    `utils/data/instances/dataverse_production`).

    """

    if user_handle == "public":
        api = NativeApi(config.BASE_URL)
    else:
        users = read_json(config.USER_FILENAME)
        api = NativeApi(config.BASE_URL, users[user_handle]["api-token"])
    tree = api.get_children(parent, children_types=data_types)
    if not os.path.isdir(os.path.join(ROOT_DIR, "data")):
        os.makedirs(os.path.join(ROOT_DIR, "data"))
        if not os.path.isdir(os.path.join(ROOT_DIR, "data", "utils")):
            os.makedirs(os.path.join(ROOT_DIR, "data", "utils"))
            if not os.path.isdir(os.path.join(ROOT_DIR, "data", "utils", user_handle)):
                os.makedirs(os.path.join(ROOT_DIR, "data", "utils", user_handle))
    write_json(os.path.join(UTILS_DATA_DIR, user_handle, filename), tree)
    if create_json:
        generate_data(tree, user_handle, filename)


def generate_data(tree: dict, user_handle: str, filename: str = "tree.json") -> None:
    """Pre-process data coming from collect data.

    Generates lists of Dataverses (`dataverses.json`),
    Datasets (`datasets.json`) and Datafiles
    (`datafiles.json`) from the tree structure (`tree.json`).
    The created lists are then used for tests
    (`test_all_dataverses()`, `test_all_datasets()`,
    `test_all_datafiles()`). The generated JSON files
    are stored inside `utils/` in the related instance
    folder.

    """
    data = read_json(os.path.join(UTILS_DATA_DIR, user_handle, filename))
    dataverses, datasets, datafiles = dataverse_tree_walker(data)
    filename_dv = os.path.join(UTILS_DATA_DIR, user_handle, config.FILENAME_DATAVERSES)
    if not os.path.isdir(os.path.join(ROOT_DIR, "data")):
        os.makedirs(os.path.join(ROOT_DIR, "data"))
        if not os.path.isdir(os.path.join(ROOT_DIR, "data", "utils")):
            os.makedirs(os.path.join(ROOT_DIR, "data", "utils"))
            if not os.path.isdir(os.path.join(ROOT_DIR, "data", "utils", user_handle)):
                os.makedirs(os.path.join(ROOT_DIR, "data", "utils", user_handle))
    if os.path.isfile(filename_dv):
        os.remove(filename_dv)
    filename_ds = os.path.join(UTILS_DATA_DIR, user_handle, config.FILENAME_DATASETS)
    if os.path.isfile(filename_ds):
        os.remove(filename_ds)
    filename_df = os.path.join(UTILS_DATA_DIR, user_handle, config.FILENAME_DATAFILES)
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
    write_json(os.path.join(UTILS_DATA_DIR, config.FILENAME_METADATA), metadata)
    print(f"- Dataverses: {len(dataverses)}")
    print(f"- Datasets: {len(datasets)}")
    print(f"- Datafiles: {len(datafiles)}")


def create_testdata(config_file: str, force: bool) -> None:
    """Create testdata defined in a config file.

    Creates a pre-defined set of testdata on your
    instance. By default, the function uses the
    AUSSDA test data repository, which is so far not
    publicly available. If `PRODUCTION` is `true`,
    this function will not execute, as long as you
    not add `--force` to the function call. This is
    to protect from unwanted changes on a production
    instance.

    """
    # Init
    if config.PRODUCTION and not force:
        print(
            "Create testdata on a PRODUCTION instance not allowed. Use --force to force it."
        )
        sys.exit()
    pid_idx = []
    users = read_json(config.USER_FILENAME)
    workflow = read_json(os.path.join(ROOT_DIR, config_file))

    # Dataverses
    for dv_conf in workflow["dataverses"]:
        dv_alias = None
        if "create" in dv_conf:
            api = NativeApi(
                config.BASE_URL, users[dv_conf["create"]["user-handle"]]["api-token"]
            )
            dv = Dataverse()
            dv_filename = os.path.join(ROOT_DIR, dv_conf["create"]["metadata-filename"])
            dv.from_json(read_file(dv_filename))
            if "update" in dv_conf["create"]:
                for key, val in dv_conf["create"]["update"].items():
                    kwargs = {key: val}
                    dv.set(kwargs)
            dv_alias = dv.get()["alias"]
            resp = api.create_dataverse(dv_conf["create"]["parent"], dv.json())

        if "publish" in dv_conf:
            api = NativeApi(
                config.BASE_URL, users[dv_conf["publish"]["user-handle"]]["api-token"]
            )
            if not dv_alias and "alias" in dv_conf["publish"]:
                dv_alias = dv_conf["publish"]["alias"]
            resp = api.publish_dataverse(dv_alias)

    # Datasets
    for ds_conf in workflow["datasets"]:
        pid = None
        if "create" in ds_conf:
            api = NativeApi(
                config.BASE_URL, users[ds_conf["create"]["user-handle"]]["api-token"]
            )
            ds = Dataset()
            ds_filename = os.path.join(ROOT_DIR, ds_conf["create"]["metadata-filename"])
            ds.from_json(read_file(ds_filename))
            if "update" in ds_conf["create"]:
                for key, val in ds_conf["create"]["update"].items():
                    kwargs = {key: val}
                    ds.set(kwargs)
            resp = api.create_dataset(dv_alias, ds.json())
            pid = resp.json()["data"]["persistentId"]
            pid_idx.append(pid)

        if "publish" in ds_conf:
            if not pid:
                print("ERROR: PID missing!")
                sys.exit()
            api = NativeApi(
                config.BASE_URL, users[ds_conf["publish"]["user-handle"]]["api-token"]
            )
            resp = api.publish_dataset(pid, release_type="major")

    # Datafiles
    for dataset_id, ds_datafiles in workflow["datafiles"].items():
        if int(dataset_id) == workflow["datasets"][int(dataset_id)]["id"]:
            pid = pid_idx[int(dataset_id)]
        else:
            print("ERROR: Dataset ID not matching.")
            sys.exit()
        for df_conf in ds_datafiles:
            if "upload" in df_conf:
                api = NativeApi(
                    config.BASE_URL,
                    users[df_conf["upload"]["user-handle"]]["api-token"],
                )
                metadata = read_json(df_conf["upload"]["metadata-filename"])
                df = Datafile()
                df.set(metadata)
                if "update" in df_conf["upload"]:
                    for key, val in df_conf["upload"]["update"].items():
                        kwargs = {key: val}
                        df.set(kwargs)
                df.set({"pid": pid})
                filename = df_conf["upload"]["filename"]
                resp = api.upload_datafile(pid, filename, df.json())
                if filename[-4:] == ".sav" or filename[-4:] == ".dta":
                    sleep(30)
                else:
                    sleep(3)
        if "publish-dataset" in df_conf:
            api = NativeApi(
                config.BASE_URL,
                users[df_conf["publish-dataset"]["user-handle"]]["api-token"],
            )
            if df_conf["publish-dataset"]:
                resp = api.publish_dataset(pid, release_type="major")


def remove_testdata(
    user_handle: str,
    parent: str,
    data_types: List[str] = ["dataverses", "datasets"],
    force: bool = False,
    parent_data_type: str = "dataverse",
    remove_parent: bool = False,
) -> None:
    """Remove testdata.

    Removes all data created by `create-testdata`.
    It recursively collects all Dataverses and Datasets
    from a passed Dataverse down (by default =
    `science`). If `PRODUCTION` is `true`, this function
    will not execute, as long as you not add `--force`
    to the function call. This is to protect from
    unwanted changes on a production instance.

    """
    if config.PRODUCTION and not force:
        print(
            "Delete testdata on a PRODUCTION instance not allowed. Use --force to force it."
        )
        sys.exit()

    user = read_json(config.USER_FILENAME)[user_handle]
    api = NativeApi(config.BASE_URL, user["api-token"])

    # Clean up
    data = api.get_children(parent, children_types=data_types)
    dataverses, datasets, = dataverse_tree_walker(data)
    if parent_data_type == "dataverse" and remove_parent:
        dataverses.append({"dataverse_alias": parent})
    for ds in datasets:
        api.destroy_dataset(ds["pid"])
    for dv in dataverses:
        api.delete_dataverse(dv["dataverse_alias"])


def create_user(user_handle: str, config_file: str, force: bool) -> None:
    """Create user.

    Create user defined in config_file and users JSON file.
    """
    # Init
    if config.PRODUCTION and not force:
        print(
            "Create user on a PRODUCTION instance not allowed. Use --force to force it."
        )
        sys.exit()
    users = read_json(config.USER_FILENAME)
    workflow = read_json(os.path.join(ROOT_DIR, config_file))

    # Users
    for user in workflow["users"]:
        if "create" in user:
            filename = os.path.join(ROOT_DIR, user["create"]["filename"])
            data = read_json(filename)
            if "update" in user["create"]:
                for key, val in user["create"]["update"].items():
                    data[key] = val
            requests.post(
                f'{config.BASE_URL}/api/builtin-users?password={users[user_handle]["password"]}&key={config.BUILTIN_USER_KEY}',
                json=data,
            )
