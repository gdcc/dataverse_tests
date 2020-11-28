import os
import requests
from time import sleep
from ..conftest import read_json


class TestDatasets:
    def test_all_datasets(self, config, test_data):
        if test_data["tests"]["all-datasets"]["test"]:
            base_url = test_data["instance"]["base-url"]
            datasets = read_json(
                os.path.join(config.INSTANCE_DATA_DIR, "datasets.json")
            )

            for ds in datasets[:2]:
                url = f"{base_url}/dataset.xhtml?persistentId={ds['pid']}"
                resp = requests.get(url, allow_redirects=True)
                sleep(3)
                assert resp.status_code == 200
                assert resp.encoding == "UTF-8"
                assert resp.url == url

                # Resolve doi.org URL
                url = f"https://doi.org/{ds['pid'][4:]}"
                resp = requests.get(url, allow_redirects=True)
                sleep(3)
                assert resp.status_code == 200
                assert resp.encoding == "UTF-8"
