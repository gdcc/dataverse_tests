import json
import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..conftest import CONFIG
from ..conftest import login_shibboleth
from ..conftest import ROOT_DIR


with open(
    os.path.join(
        ROOT_DIR,
        "src/dvtests/testing/data",
        CONFIG.INSTANCE,
        "custom/aussda/system/testdata_authentication.json",
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
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        selenium = login_shibboleth(selenium, config,)
        navbar_user = wait.until(
            EC.element_to_be_clickable((By.ID, "userDisplayInfoTitle"))
        )

        # Act
        # Assert
        assert selenium.title == expected["title"]
        assert navbar_user.text == config.USER_SHIBBOLETH_NAME

        # Cleanup
