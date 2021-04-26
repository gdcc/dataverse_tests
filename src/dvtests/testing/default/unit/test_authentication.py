import json
import os
from time import sleep

import pytest
from selenium.webdriver.common.by import By

from ..conftest import BASE_URL
from ..conftest import INSTANCE
from ..conftest import login_normal_user
from ..conftest import login_shibboleth_user
from ..conftest import ROOT_DIR


with open(
    os.path.join(
        ROOT_DIR,
        "src/dvtests/testing/data",
        INSTANCE,
        "default/unit/testdata_authentication.json",
    )
) as json_file:
    testdata = json.load(json_file)


class TestShibboleth:
    @pytest.mark.v4_18_1
    @pytest.mark.v4_20
    @pytest.mark.parametrize(
        "test_input,expected", testdata["shibboleth"]["interface-valid"]
    )
    def test_interface_valid(self, session, test_input, expected):
        """Test Shibboleth interface."""
        # Arrange
        url = f'{BASE_URL}{test_input["url"]}'

        # Act
        resp = session.get(url)

        # Assert
        assert resp.url == url
        assert resp.status_code == 200
        assert resp.headers["Content-Type"] == expected["content-type"]
        # Cleanup
