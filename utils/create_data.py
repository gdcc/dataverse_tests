import glob
import os
from time import sleep

from pyDataverse.api import NativeApi
from pyDataverse.utils import read_file, read_json
from pyDataverse.models import Dataverse, Dataset, Datafile


ROOT_DIR = dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


if __name__ == "__main__":
    print("START --------------------------")

    INSTANCE = os.getenv("INSTANCE")
    BASE_URL = os.getenv("BASE_URL")
    API_TOKEN = os.getenv("API_TOKEN")
    lst_pids = []
    api = NativeApi(BASE_URL, API_TOKEN)

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

    for filepath in json_filenames[:1]:
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

    # Set access rights of Datafiles
    if False:
        pass

    print("END --------------------------")
