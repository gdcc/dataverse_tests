from time import sleep

import pytest
from selenium.webdriver.common.by import By

from ..conftest import login_normal_user


class TestUserProfile:
    @pytest.mark.v4_18_1
    @pytest.mark.selenium
    def test_navigate(self, test_config, config, selenium):
        """

        Input
        * base url

        Expected result
        * title

        """
        test_cfg = test_config["tests"]["user-profile-navigate"]
        instance_cfg = test_config["instance"]

        selenium = login_normal_user(
            selenium, test_config, config, config.USER_NORMAL, config.USER_NORMAL_PWD,
        )

        assert instance_cfg["title"] == selenium.title
        selenium.find_element(By.ID, "userDisplayInfoTitle").click()
        sleep(3)
        selenium.find_element(By.LINK_TEXT, "My Data").click()
        sleep(3)
        assert test_cfg["title"] == selenium.title
        selenium.find_element(By.LINK_TEXT, "Notifications").click()
        sleep(3)
        selenium.find_element(By.LINK_TEXT, "Account Information").click()
        sleep(3)
        selenium.find_element(By.LINK_TEXT, "API Token").click()
        sleep(3)
