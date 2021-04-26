import os
from time import sleep

import pytest
import requests

from ..conftest import get_instance_dir
from ..conftest import login_normal_user
from ..conftest import read_json


class TestDatasets:
    @pytest.mark.v4_18_1
    @pytest.mark.selenium
    def test_all_datasets(self, config, test_config, selenium):
        """

        Input
        * base url
        * datasets pids

        Expected result
        * datafile
            * url

        """
        instance_dir = get_instance_dir(config)
        base_url = test_config["instance"]["base-url"]
        datasets = read_json(os.path.join(instance_dir, config.FILENAME_DATASETS))
        selenium = login_normal_user(
            selenium,
            test_config,
            config,
            config.USER_SUPERUSER,
            config.USER_SUPERUSER_PWD,
        )

        for ds in datasets:
            url = f"{base_url}/dataset.xhtml?persistentId={ds['pid']}"
            selenium.get(url)
            sleep(1)
            assert url == selenium.current_url

    @pytest.mark.v4_18_1
    def test_all_doiorg_pages(self, config, test_config):
        """

        Input
        * base url
        * dataset pids

        Expected result
        * dataset
            * url
            * status code

        """
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
