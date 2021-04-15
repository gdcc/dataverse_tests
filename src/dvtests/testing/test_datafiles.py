import os
from time import sleep

import pytest
import requests

from ..conftest import get_instance_dir
from ..conftest import login_normal_user
from ..conftest import read_json


class TestDatafiles:
    def test_all_datafiles(self, config, test_config, firefox):
        if not test_config["tests"]["all-datafiles"]["test"]:
            pytest.skip("Test not configured to be executed.")

        instance_dir = get_instance_dir(config)
        base_url = test_config["instance"]["base-url"]
        datafiles = read_json(os.path.join(instance_dir, config.FILENAME_DATAFILES))
        firefox = login_normal_user(
            firefox,
            test_config,
            config,
            config.USER_SUPERUSER,
            config.USER_SUPERUSER_PWD,
        )

        for df in datafiles:
            url = f"{base_url}/file.xhtml?fileId={df['datafile_id']}&version=:latest"
            firefox.get(url)
            sleep(1)
            assert url == firefox.current_url
