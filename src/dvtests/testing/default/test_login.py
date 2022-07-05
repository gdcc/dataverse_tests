import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..conftest import INSTALLATION_TESTING_CONFIG_DIR
from ..conftest import read_json


test_config = read_json(
    os.path.join(INSTALLATION_TESTING_CONFIG_DIR, "default/test_login.json",)
)


class TestLogin:
    @pytest.mark.v4_20
    @pytest.mark.v5_2
    @pytest.mark.v5_6
    @pytest.mark.selenium
    @pytest.mark.parametrize(
        "homepage_logged_in", test_config["login"]["valid"]["users"], indirect=True,
    )
    @pytest.mark.parametrize(
        "test_input,expected", test_config["login"]["valid"]["input-expected"],
    )
    def test_valid(
        self, config, homepage_logged_in, xpaths, users, test_input, expected
    ):
        """Test normal login procedure."""
        # Arrange
        selenium, user_handle = homepage_logged_in
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        # Act
        navbar_user = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, xpaths["navbar-user-display-info-title"])
            )
        )
        # Assert
        assert selenium.title == expected["title"]
        assert (
            navbar_user.text
            == users[user_handle]["firstName"] + " " + users[user_handle]["lastName"]
        )
        # Cleanup
