import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..conftest import read_json
from ..conftest import TEST_CONFIG_DATA_DIR


test_config = read_json(
    os.path.join(
        TEST_CONFIG_DATA_DIR, "default/system/test-config_authentication.json",
    )
)


class TestNormalLogin:
    @pytest.mark.v4_20
    @pytest.mark.selenium
    @pytest.mark.parametrize(
        "homepage_logged_in",
        test_config["normal-login"]["login-valid"]["users"],
        indirect=True,
    )
    @pytest.mark.parametrize(
        "test_input,expected",
        test_config["normal-login"]["login-valid"]["input-expected"],
    )
    def test_login_valid(self, config, homepage_logged_in, users, test_input, expected):
        """Test normal login procedure."""
        # Arrange
        selenium, user_handle = homepage_logged_in
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        # Act
        navbar_user = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[@id='userDisplayInfoTitle']"))
        )
        # Assert
        assert selenium.title == expected["title"]
        assert (
            navbar_user.text
            == users[user_handle]["given-name"]
            + " "
            + users[user_handle]["family-name"]
        )
        # Cleanup
