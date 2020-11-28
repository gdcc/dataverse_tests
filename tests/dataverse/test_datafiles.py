import os
from time import sleep
from ..conftest import read_json


class TestDatafiles:
    def test_all_datafiles(self, config, test_data, firefox):
        if test_data["tests"]["all-datafiles"]["test"]:
            base_url = test_data["instance"]["base-url"]
            datafiles = read_json(os.path.join(config.DATA_DIR, "datafiles.json"))

            for df in datafiles:
                url = (
                    f"{base_url}/file.xhtml?fileId={df['datafile_id']}&version=:latest"
                )
                firefox.get(url)
                sleep(3)
                assert df["filename"] in firefox.title
                assert url == firefox.current_url
