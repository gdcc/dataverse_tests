import os
from time import sleep

import pytest
import requests

from ..conftest import get_instance_dir
from ..conftest import login_normal_user
from ..conftest import read_json


class TestDatafiles:
    @pytest.mark.v4_18_1
    @pytest.mark.selenium
    def test_all_datafiles(self, config, test_config, selenium):
        """

        Input
        * base url
        * datafiles

        Expected result
        * datafile
            * url

        """
        instance_dir = get_instance_dir(config)
        base_url = test_config["instance"]["base-url"]
        datafiles = read_json(os.path.join(instance_dir, config.FILENAME_DATAFILES))
        selenium = login_normal_user(
            selenium,
            test_config,
            config,
            config.USER_SUPERUSER,
            config.USER_SUPERUSER_PWD,
        )

        for df in datafiles:
            url = f"{base_url}/file.xhtml?fileId={df['datafile_id']}&version=:latest"
            selenium.get(url)
            sleep(1)
            assert url == selenium.current_url
