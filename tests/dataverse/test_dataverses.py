import os
from time import sleep
from ..conftest import read_json


class TestDataverses:
    def test_all_dataverses(self, config, test_data, firefox):
        if test_data["tests"]["all-dataverses"]["test"]:
            base_url = test_data["instance"]["base-url"]
            dataverses = read_json(
                os.path.join(config.INSTANCE_DATA_DIR, "dataverses.json")
            )

            for dv in dataverses:
                url = f"{base_url}/dataverse.xhtml?alias={dv['dataverse_alias']}"
                firefox.get(url)
                sleep(1)
                assert dv["title"] in firefox.title
                assert url == firefox.current_url

                url = f"{base_url}/dataverse/{dv['dataverse_alias']}"
                firefox.get(url)
                sleep(1)
                assert dv["title"] in firefox.title
                assert url == firefox.current_url
