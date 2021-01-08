import os
from time import sleep

import pytest
import requests

from ..conftest import get_instance_dir, read_json


class TestDatafiles:
    def test_all_datafiles(self, config, test_config):
        if not test_config["tests"]["all-datafiles"]["test"]:
            pytest.skip("Test not configured to be executed.")

        instance_dir = get_instance_dir(config)
        base_url = test_config["instance"]["base-url"]
        datafiles = read_json(os.path.join(instance_dir, config.FILENAME_DATAFILES))

        for df in datafiles:
            url = f"{base_url}/file.xhtml?fileId={df['datafile_id']}&version=:latest"
            resp = requests.get(url, allow_redirects=True)
            # sleep(3)
            assert resp.status_code == 200
            assert resp.encoding == "UTF-8"
            assert resp.url == url
