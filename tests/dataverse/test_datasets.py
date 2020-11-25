import os
import requests
from time import sleep
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(os.path.dirname(dir_path), "data")


class TestDatasets:
    def test_all_datasets(self):
        data = read_json(os.path.join(data_path, "datasets.json"))
        for ds in data:
            url = f"https://data.aussda.at/dataset.xhtml?persistentId={ds['pid']}"
            resp = requests.get(url, allow_redirects=True)
            sleep(1)
            assert resp.status_code == 200
            assert resp.encoding == "UTF-8"
            assert resp.url == url

            # Resolve doi.org URL
            url = f"https://doi.org/{ds['pid'][4:]}"
            resp = requests.get(url, allow_redirects=True)
            sleep(1)
            assert resp.status_code == 200
            assert resp.encoding == "UTF-8"
