import os
from time import sleep

import pytest
import requests

from ..conftest import get_instance_dir, read_json, login_normal_user


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

        for ds in datasets:
            url = f"{base_url}/dataset.xhtml?persistentId={ds['pid']}"
            firefox.get(url)
            sleep(1)
            assert url == firefox.current_url

    def test_all_doiorg_pages(self, config, test_config, firefox):
        if not test_config["tests"]["all-datasets"]["test"]:
            pytest.skip("Test not configured to be executed.")

        instance_dir = get_instance_dir(config)
        datasets = read_json(os.path.join(instance_dir, config.FILENAME_DATASETS))
        firefox = login_normal_user(
            firefox,
            test_config,
            config,
            config.USER_SUPERUSER,
            config.USER_SUPERUSER_PWD,
        )

        # Resolve doi.org URL
        for ds in datasets:
            url = f"https://doi.org/{ds['pid'][4:]}"
            firefox.get(url)
            sleep(3)
            assert url == firefox.current_url
