import json
import os

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
        "default/system/testdata_authentication.json",
    )
) as json_file:
    testdata = json.load(json_file)


class TestShibboleth:
    @pytest.mark.v4_18_1
    @pytest.mark.v4_20
    @pytest.mark.selenium
    @pytest.mark.parametrize("expected", testdata["shibboleth"]["login-valid"])
    def test_login_valid(self, config, selenium, expected):
        """Test Shibboleth login procedure."""
        # Arrange
        # Act
        selenium = login_shibboleth_user(
            selenium,
            BASE_URL,
            config.WINDOW_WIDTH,
            config.WINDOW_HEIGHT,
            config.USER_SHIBBOLETH,
            config.USER_SHIBBOLETH_PWD,
            config.USER_SHIBBOLETH_NAME,
        )

        # Assert
        assert selenium.title == expected["title"]
        assert (
            selenium.find_element(By.ID, "userDisplayInfoTitle").text
            == config.USER_SHIBBOLETH_NAME
        )
        # Cleanup


class TestNormalLogin:
    @pytest.mark.v4_18_1
    @pytest.mark.v4_20
    @pytest.mark.selenium
    @pytest.mark.parametrize(
        "test_input,expected", testdata["normal-login"]["login-valid"]
    )
    def test_login(self, config, selenium, test_input, expected):
        """Test normal login procedure."""
        # Arrange
        # Act
        selenium = login_normal_user(
            selenium,
            test_input["login-mode"],
            config.WINDOW_WIDTH,
            config.WINDOW_HEIGHT,
            config.USER_NORMAL,
            config.USER_NORMAL_PWD,
        )

        # Assert
        assert selenium.title == expected["title"]
        assert (
            selenium.find_element(By.ID, "userDisplayInfoTitle").text
            == config.USER_NORMAL_NAME
        )
        # Cleanup
