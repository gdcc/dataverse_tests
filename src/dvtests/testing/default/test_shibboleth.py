import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..conftest import INSTALLATION_TESTING_CONFIG_DIR
from ..conftest import read_json


test_config = read_json(
    os.path.join(INSTALLATION_TESTING_CONFIG_DIR, "default/test_shibboleth.json",)
)


class TestShibboleth:
    @pytest.mark.v4_20
    @pytest.mark.v5_6
    @pytest.mark.parametrize(
        "test_input,expected",
        test_config["shibboleth"]["interface-valid"]["input-expected"],
    )
    def test_interface_valid(self, config, session, test_input, expected):
        """Test Shibboleth interface."""
        # Arrange
        url = f'{config.BASE_URL}{test_input["url"]}'
        # Act
        resp = session.get(url)
        # Assert
        assert resp.url == url
        assert resp.status_code == 200
        assert resp.headers["Content-Type"] == expected["content-type"]
        # Cleanup
