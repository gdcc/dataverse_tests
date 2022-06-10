import os
from time import sleep

import pytest
import requests
from selenium.webdriver.common.by import By

from ..conftest import click_cookie_rollbar
from ..conftest import get_instance_dir
from ..conftest import read_json


class TestHeader:
    @pytest.mark.v4_18_1
    @pytest.mark.selenium
    def test_contact(self, test_config, config, selenium):
        """

        Input
        *

        Expected result
        *

        """
        # Arrange
        # Act
        # Assert
        # Cleanup
        test_cfg = test_config["tests"]["header"]["contact"]
        instance_cfg = test_config["instance"]

        if not test_cfg["test"]:
            pytest.skip("Test not configured to be executed.")

        base_url = instance_cfg["base-url"]

        selenium.get(base_url)
        sleep(3)
        selenium.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        selenium.find_element(By.CLASS_NAME, "btn-contact").click()
        sleep(3)

    @pytest.mark.v4_18_1
    @pytest.mark.selenium
    def test_branding(self, test_config, config, selenium):
        """

        Input
        *

        Expected result
        *

        """
        # Arrange
        # Act
        # Assert
        # Cleanup
        test_cfg = test_config["tests"]["header"]["branding"]
        instance_cfg = test_config["instance"]

        base_url = instance_cfg["base-url"]

        selenium.get(base_url)
        sleep(3)
        selenium.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        selenium.find_element(By.CSS_SELECTOR, ".navbar-header .navbar-brand").click()
        sleep(3)
        assert instance_cfg["title"] in selenium.title
        assert selenium.current_url == test_cfg["url"]

    @pytest.mark.v4_18_1
    @pytest.mark.selenium
    def test_about(self, config, test_config, selenium):
        """

        Input
        *

        Expected result
        *

        """
        # Arrange
        # Act
        # Assert
        # Cleanup
        test_cfg = test_config["tests"]["header"]["about"]
        instance_cfg = test_config["instance"]

        base_url = instance_cfg["base-url"]

        selenium.get(base_url)
        sleep(3)
        selenium.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        vars = {}
        vars["window_handles"] = selenium.window_handles
        selenium.find_element(By.LINK_TEXT, "About").click()
        sleep(3)
        vars["root"] = selenium.current_window_handle
        print(selenium.window_handles)
        vars["website"] = selenium.window_handles[1]
        selenium.switch_to.window(vars["website"])
        sleep(3)
        assert selenium.current_url == test_cfg["url"]
