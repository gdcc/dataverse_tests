import os
import requests
from time import sleep
from ..conftest import read_json, get_instance_dir


class TestDatasets:
    def test_all_datasets(self, config, test_config):
        if test_config["tests"]["all-datasets"]["test"]:
            instance_dir = get_instance_dir(config)
            base_url = test_config["instance"]["base-url"]
            datasets = read_json(os.path.join(instance_dir, config.FILENAME_DATASETS))

            for ds in datasets:
                url = f"{base_url}/dataset.xhtml?persistentId={ds['pid']}"
                resp = requests.get(url, allow_redirects=True)
                sleep(3)
                print(url)
                assert resp.status_code == 200
                assert resp.encoding == "UTF-8"
                assert resp.url == url

                # Resolve doi.org URL
                url = f"https://doi.org/{ds['pid'][4:]}"
                resp = requests.get(url, allow_redirects=True)
                sleep(3)
                assert resp.status_code == 200
                assert resp.encoding == "UTF-8"
