import os
from time import sleep
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(os.path.dirname(dir_path), "data")


class TestDataverses:
    def test_all_dataverses(self, firefox):
        data = read_json(os.path.join(data_path, "dataverses.json"))
        for dv in data:
            url = (
                f"https://data.aussda.at/dataverse.xhtml?alias={dv['dataverse_alias']}"
            )
            firefox.get(url)
            sleep(1)
            assert dv["title"] in firefox.title
            assert url == firefox.current_url

            url = f"https://data.aussda.at/dataverse/{dv['dataverse_alias']}"
            firefox.get(url)
            sleep(1)
            assert dv["title"] in firefox.title
            assert url == firefox.current_url
