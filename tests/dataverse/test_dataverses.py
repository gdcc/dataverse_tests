import os
from time import sleep
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(os.path.dirname(dir_path), "data")


class TestDataverses:
    def test_all_dataverses(self, firefox):
        INSTANCE = os.getenv("INSTANCE")
        data = read_json(
            os.path.join(data_path, f"instances/{INSTANCE}/test-data.json")
        )
        base_url = data["instance"]["base-url"]

        if data["tests"]["all-dataverses"]:
            dataverses = read_json(
                os.path.join(data_path, f"instances/{INSTANCE}/dataverses.json")
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
