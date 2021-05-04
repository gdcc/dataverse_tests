import json
import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..conftest import login_normal
from ..conftest import TESTING_DATA_DIR


with open(
    os.path.join(TESTING_DATA_DIR, "default/system/testdata_authentication.json",)
) as json_file:
    testdata = json.load(json_file)


class TestNormalLogin:
    @pytest.mark.v4_20
    @pytest.mark.selenium
    @pytest.mark.parametrize(
        "test_input,expected", testdata["normal-login"]["login-valid"]
    )
    def test_login_valid(self, config, selenium, users, test_input, expected):
        """Test normal login procedure."""
        # Arrange
        # Act
        login_normal(
            selenium,
            config.BASE_URL,
            config.LOGIN_OPTIONS,
            test_input["user-handle"],
            users[test_input["user-handle"]]["password"],
            config.MAX_WAIT_TIME,
        )
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        navbar_user = wait.until(
            EC.element_to_be_clickable((By.ID, "userDisplayInfoTitle"))
        )
        # Assert
        assert selenium.title == expected["title"]
        assert navbar_user.text == users[test_input["user-handle"]]["name"]
        # Cleanup
