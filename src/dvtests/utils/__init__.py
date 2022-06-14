import os
import sys
from json import load
from time import sleep
from typing import Dict
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
    CONFIG = UtilsSettings(_env_file=os.getenv("ENV_FILE"))
else:
    CONFIG = UtilsSettings()
ROOT_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)
UTILS_DATA_DIR = os.path.join(ROOT_DIR, "data", CONFIG.INSTANCE)
INSTALLATION_DATA_DIR = os.path.join(ROOT_DIR, "data", CONFIG.INSTANCE)
with open(os.path.join(ROOT_DIR, CONFIG.USER_FILENAME), "r", encoding="utf-8") as f:
    USERS = load(f)


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
        api = NativeApi(CONFIG.BASE_URL)
    else:
        users = read_json(CONFIG.USER_FILENAME)
        api = NativeApi(CONFIG.BASE_URL, users[user_handle]["api-token"])
    tree = api.get_children(parent, children_types=data_types)
    if not os.path.isdir(os.path.join(ROOT_DIR, "data")):
        os.makedirs(os.path.join(ROOT_DIR, "data"))
    if not os.path.isdir(os.path.join(INSTALLATION_DATA_DIR)):
        os.makedirs(os.path.join(INSTALLATION_DATA_DIR))
    if not os.path.isdir(os.path.join(INSTALLATION_DATA_DIR, user_handle)):
        os.makedirs(os.path.join(INSTALLATION_DATA_DIR, user_handle))
    if not os.path.isdir(os.path.join(ROOT_DIR, "data", user_handle, "utils")):
        os.makedirs(os.path.join(ROOT_DIR, "data", user_handle, "utils"))
    write_json(os.path.join(UTILS_DATA_DIR, user_handle, filename), tree)
    if create_json:
        generate_data(user_handle, filename)


def generate_data(user_handle: str = "public", filename: str = "tree.json") -> None:
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
    filename_dv = os.path.join(UTILS_DATA_DIR, user_handle, CONFIG.FILENAME_DATAVERSES)
    if not os.path.isdir(os.path.join(ROOT_DIR, "data")):
        os.makedirs(os.path.join(ROOT_DIR, "data"))
        if not os.path.isdir(os.path.join(ROOT_DIR, "data", "utils")):
            os.makedirs(os.path.join(ROOT_DIR, "data", "utils"))
            if not os.path.isdir(os.path.join(ROOT_DIR, "data", "utils", user_handle)):
                os.makedirs(os.path.join(ROOT_DIR, "data", "utils", user_handle))
    if os.path.isfile(filename_dv):
        os.remove(filename_dv)
    filename_ds = os.path.join(UTILS_DATA_DIR, user_handle, CONFIG.FILENAME_DATASETS)
    if os.path.isfile(filename_ds):
        os.remove(filename_ds)
    filename_df = os.path.join(UTILS_DATA_DIR, user_handle, CONFIG.FILENAME_DATAFILES)
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
    write_json(
        os.path.join(UTILS_DATA_DIR, user_handle, CONFIG.FILENAME_METADATA), metadata
    )
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
    if CONFIG.PRODUCTION and not force:
        print(
            "Create testdata on a PRODUCTION instance not allowed. Use --force to force it."
        )
        sys.exit()
    users = read_json(CONFIG.USER_FILENAME)
    workflow = read_json(os.path.join(ROOT_DIR, config_file))
    dv_dvtests_id_2_alias: Dict = {}
    ds_dvtests_id_2_pid: Dict = {}

    for count, action in enumerate(workflow):
        # Create Dataverse
        if action["data-type"] == "dataverse" and action["action"] == "create":
            api = NativeApi(CONFIG.BASE_URL, users[action["user-handle"]]["api-token"])
            dv = Dataverse()
            dv_metadata_filename = os.path.join(
                ROOT_DIR, action["metadata"]["filename"]
            )
            dv.from_json(read_file(dv_metadata_filename), validate=False)
            if "update" in action["metadata"]:
                for key, val in action["metadata"]["update"].items():
                    kwargs = {key: val}
                    dv.set(kwargs)
            parent_id = action["parent-id"]
            if "parent-id-type" in action:
                if "parent-id" in action:
                    if action["parent-id-type"] == "dvtests":
                        parent_id = dv_dvtests_id_2_alias[action["parent-id"]]
            resp = api.create_dataverse(parent_id, dv.json(validate=False))
            if "id-type" in action:
                if "id" in action:
                    if action["id-type"] == "dvtests":
                        dv_dvtests_id_2_alias[action["id"]] = dv.get()["alias"]

        # Publish Dataverse
        if action["data-type"] == "dataverse" and action["action"] == "publish":
            api = NativeApi(CONFIG.BASE_URL, users[action["user-handle"]]["api-token"])
            dv_id = action["id"]
            if "id-type" in action:
                if "id" in action:
                    if action["id-type"] == "dvtests":
                        dv_id = dv_dvtests_id_2_alias[action["id"]]
            resp = api.publish_dataverse(dv_id)

        # Create Dataset
        if action["data-type"] == "dataset" and action["action"] == "create":
            api = NativeApi(CONFIG.BASE_URL, users[action["user-handle"]]["api-token"])
            ds = Dataset()
            ds_metadata_filename = os.path.join(
                ROOT_DIR, action["metadata"]["filename"]
            )
            ds.from_json(read_file(ds_metadata_filename), validate=False)
            if "update" in action["metadata"]:
                for key, val in action["metadata"]["update"].items():
                    kwargs = {key: val}
                    ds.set(kwargs)
            if "parent-id-type" in action:
                if "parent-id" in action:
                    if action["parent-id-type"] == "dvtests":
                        parent_id = dv_dvtests_id_2_alias[action["parent-id"]]
            else:
                parent_id = action["parent-id"]
            resp = api.create_dataset(parent_id, ds.json(validate=False))
            pid = resp.json()["data"]["persistentId"]
            if "id-type" in action:
                if "id" in action:
                    if action["id-type"] == "dvtests":
                        ds_dvtests_id_2_pid[action["id"]] = pid

        # Publish Dataset
        if action["data-type"] == "dataset" and action["action"] == "publish":
            api = NativeApi(CONFIG.BASE_URL, users[action["user-handle"]]["api-token"])
            pid = action["id"]
            if "id-type" in action:
                if "id" in action:
                    if action["id-type"] == "dvtests":
                        pid = ds_dvtests_id_2_pid[action["id"]]
            check_dataset_lock(api, pid)
            resp = api.publish_dataset(pid, release_type=action["release-type"])

        # Upload Datafile
        if action["data-type"] == "datafile" and action["action"] == "upload":
            api = NativeApi(CONFIG.BASE_URL, users[action["user-handle"]]["api-token"])
            filename = action["filename"]
            parent_pid = action["parent-id"]
            if "parent-id-type" in action:
                if "parent-id" in action:
                    if action["parent-id-type"] == "dvtests":
                        parent_pid = ds_dvtests_id_2_pid[action["parent-id"]]
            check_dataset_lock(api, parent_pid)
            if "metadata" in action:
                if "filename" in action["metadata"]:
                    metadata = read_json(action["metadata"]["filename"])
                    df = Datafile()
                    df.set(metadata)
                    if "update" in action["metadata"]:
                        for key, val in action["metadata"]["update"].items():
                            kwargs = {key: val}
                            df.set(kwargs)
                    df.set({"pid": parent_pid})
                    resp = api.upload_datafile(
                        parent_pid, filename, df.json(validate=False)
                    )
                else:
                    resp = api.upload_datafile(parent_pid, filename)
            else:
                resp = api.upload_datafile(parent_pid, filename)


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
    if CONFIG.PRODUCTION and not force:
        print(
            "Delete testdata on a PRODUCTION instance not allowed. Use --force to force it."
        )
        sys.exit()
    user = read_json(CONFIG.USER_FILENAME)[user_handle]
    api = NativeApi(CONFIG.BASE_URL, user["api-token"])

    # Clean up
    # data_types = ["dataverses", "datasets"]
    data = api.get_children(
        parent, parent_type=parent_data_type, children_types=data_types
    )
    dataverses, datasets, datafiles, = dataverse_tree_walker(data)
    dataverses.reverse()
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
    if CONFIG.PRODUCTION and not force:
        print(
            "Create user on a PRODUCTION instance not allowed. Use --force to force it."
        )
        sys.exit()
    users = read_json(CONFIG.USER_FILENAME)
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
                f'{CONFIG.BASE_URL}/api/builtin-users?password={users[user_handle]["password"]}&key={CONFIG.BUILTIN_USER_KEY}',
                json=data,
            )


def check_dataset_lock(api, pid, is_pid=True):
    """Check if dataset is locked."""
    resp = api.get_dataset_lock(pid)
    if resp.json()["data"]:
        sleep(2)
        check_dataset_lock(api, pid)
