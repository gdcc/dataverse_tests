import os
from time import sleep

import pytest

from ..conftest import get_instance_dir
from ..conftest import login_normal_user
from ..conftest import read_json


class TestDataverses:
    @pytest.mark.v4_18_1
    @pytest.mark.selenium
    def test_all_dataverses(self, config, test_config, selenium):
        """

        TODO
        * remove selenium

        Input
        * base url
        * dataverse aliases

        Expected result
        * dataverses
            * url

        """
        instance_dir = get_instance_dir(config)
        base_url = test_config["instance"]["base-url"]
        dataverses = read_json(os.path.join(instance_dir, config.FILENAME_DATAVERSES))
        selenium = login_normal_user(
            selenium,
            test_config,
            config,
            config.USER_SUPERUSER,
            config.USER_SUPERUSER_PWD,
        )

        for dv in dataverses:
            url = f"{base_url}/dataverse.xhtml?alias={dv['dataverse_alias']}"
            selenium.get(url)
            sleep(1)
            assert url == selenium.current_url

            url = f"{base_url}/dataverse/{dv['dataverse_alias']}"
            selenium.get(url)
            sleep(1)
            assert url == selenium.current_url
