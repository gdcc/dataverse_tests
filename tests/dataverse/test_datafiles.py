import os
from time import sleep
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(os.path.dirname(dir_path), "data")


class TestDatafiles:
    def test_all_datafiles(self, firefox):
        INSTANCE = os.getenv("INSTANCE")
        data = read_json(
            os.path.join(data_path, f"instances/{INSTANCE}/test-data.json")
        )
        base_url = data["instance"]["base-url"]

        if data["tests"]["all-datafiles"]:
            datafiles = read_json(
                os.path.join(data_path, f"instances/{INSTANCE}/datafiles.json")
            )

            for df in datafiles:
                url = (
                    f"{base_url}/file.xhtml?fileId={df['datafile_id']}&version=:latest"
                )
                firefox.get(url)
                sleep(1)
                assert df["filename"] in firefox.title
                assert url == firefox.current_url
