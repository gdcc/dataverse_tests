import os
from time import sleep

import pytest
import requests

from ..conftest import get_instance_dir
from ..conftest import login_normal_user
from ..conftest import read_json


class TestDatasets:
    def test_all_datasets(self, config, test_config, firefox):
        if not test_config["tests"]["all-datasets"]["test"]:
            pytest.skip("Test not configured to be executed.")

        instance_dir = get_instance_dir(config)
        base_url = test_config["instance"]["base-url"]
        datasets = read_json(os.path.join(instance_dir, config.FILENAME_DATASETS))
        firefox = login_normal_user(
            firefox,
            test_config,
            config,
            config.USER_SUPERUSER,
            config.USER_SUPERUSER_PWD,
        )

        for ds in datasets:  # TODO: remove list subscripting
            url = f"{base_url}/dataset.xhtml?persistentId={ds['pid']}"
            firefox.get(url)
            sleep(1)
            assert url == firefox.current_url

    def test_all_doiorg_pages(self, config, test_config):
        if not test_config["tests"]["all-datasets"]["test"]:
            pytest.skip("Test not configured to be executed.")

        instance_dir = get_instance_dir(config)
        datasets = read_json(os.path.join(instance_dir, config.FILENAME_DATASETS))
        base_url = test_config["instance"]["base-url"]

        # Resolve doi.org URL
        for ds in datasets:
            url_start = f"https://doi.org/{ds['pid'][4:]}"
            url_end = f"{base_url}/dataset.xhtml?persistentId={ds['pid']}"
            resp = requests.get(url_start)
            sleep(3)
            assert resp.status_code == 200
            assert url_end == resp.current_url
