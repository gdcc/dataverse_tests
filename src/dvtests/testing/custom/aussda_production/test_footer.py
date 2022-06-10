import os
from time import sleep

import pytest
import requests
from selenium.webdriver.common.by import By

from ..conftest import custom_custom_click_cookie_rollbar
from ..conftest import read_json


class TestCustomizedFooter:
    @pytest.mark.v4_18_1
    @pytest.mark.selenium
    def test_privacy_policy(self, config, selenium):
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
        test_cfg = config["tests"]["footer"]["privacy-policy"]
        instance_cfg = config["instance"]

        base_url = instance_cfg["base-url"]
        selenium.get(base_url)
        sleep(3)
        selenium.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        if instance_cfg["has-cookie-rollbar"]:
            selenium = custom_click_cookie_rollbar(selenium)
        selenium.find_element(By.LINK_TEXT, test_cfg["name"],).click()
        sleep(3)
        assert test_cfg["url"] == selenium.current_url

    @pytest.mark.v4_18_1
    @pytest.mark.selenium
    def test_policies(self, test_config, config, selenium):
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
        test_cfg = test_config["tests"]["footer"]["policies"]
        instance_cfg = test_config["instance"]

        base_url = instance_cfg["base-url"]

        selenium.get(base_url)
        sleep(3)
        selenium.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        if instance_cfg["has-cookie-rollbar"]:
            selenium = custom_click_cookie_rollbar(selenium)
        selenium.find_element(By.LINK_TEXT, test_cfg["name"],).click()
        sleep(3)
        assert test_cfg["url"] == selenium.current_url

    @pytest.mark.v4_18_1
    @pytest.mark.selenium
    def test_imprint(self, test_config, config, selenium):
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
        test_cfg = test_config["tests"]["footer"]["imprint"]
        instance_cfg = test_config["instance"]

        base_url = instance_cfg["base-url"]
        selenium.get(base_url)
        sleep(3)
        selenium.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        if instance_cfg["has-cookie-rollbar"]:
            selenium = custom_click_cookie_rollbar(selenium)
        selenium.find_element(By.LINK_TEXT, test_cfg["name"],).click()
        sleep(3)
        assert test_cfg["url"] == selenium.current_url

    @pytest.mark.v4_18_1
    @pytest.mark.selenium
    def test_termsofservice(self, test_config, config, selenium):
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
        test_cfg = test_config["tests"]["footer"]["terms-of-service"]
        instance_cfg = test_config["instance"]

        base_url = instance_cfg["base-url"]
        selenium.get(base_url)
        sleep(3)
        selenium.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        if instance_cfg["has-cookie-rollbar"]:
            selenium = custom_click_cookie_rollbar(selenium)
        selenium.find_element(By.LINK_TEXT, test_cfg["name"],).click()
        sleep(3)
        assert test_cfg["url"] == selenium.current_url

    @pytest.mark.v4_18_1
    @pytest.mark.selenium
    def test_cessda(self, test_config, config, selenium):
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
        test_cfg = test_config["tests"]["footer"]["cessda"]
        instance_cfg = test_config["instance"]

        base_url = instance_cfg["base-url"]
        selenium.get(base_url)
        sleep(3)
        selenium.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        if instance_cfg["has-cookie-rollbar"]:
            selenium = custom_click_cookie_rollbar(selenium)
        selenium.find_element(By.LINK_TEXT, test_cfg["name"],).click()
        sleep(3)
        assert test_cfg["url"] == selenium.current_url

    @pytest.mark.v4_18_1
    @pytest.mark.selenium
    @pytest.mark.parametrize(
        "test_input,expected", test_config["dataverse"]["valid"]["input-expected"]
    )
    def test_coretrustseal(self, config, selenium):
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
        test_cfg = test_config["tests"]["footer"]["core-trust-seal"]
        instance_cfg = test_config["instance"]

        base_url = instance_cfg["base-url"]
        selenium.get(base_url)
        sleep(3)
        selenium.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        if instance_cfg["has-cookie-rollbar"]:
            selenium = custom_click_cookie_rollbar(selenium)
        selenium.find_element(By.LINK_TEXT, test_cfg["name"],).click()
        sleep(3)
        assert test_cfg["url"] == selenium.current_url

    @pytest.mark.v4_18_1
    @pytest.mark.selenium
    def test_website(self, test_config, config, selenium):
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
        test_cfg = test_config["tests"]["footer"]["website"]
        instance_cfg = test_config["instance"]

        base_url = instance_cfg["base-url"]
        selenium.get(base_url)
        sleep(3)
        selenium.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        if instance_cfg["has-cookie-rollbar"]:
            selenium = custom_click_cookie_rollbar(selenium)
        selenium.find_element(By.LINK_TEXT, test_cfg["name"],).click()
        sleep(3)
        assert test_cfg["url"] == selenium.current_url

    @pytest.mark.v4_18_1
    @pytest.mark.selenium
    def test_twitter(self, test_config, config, selenium):
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
        test_cfg = test_config["tests"]["footer"]["twitter"]
        instance_cfg = test_config["instance"]

        base_url = instance_cfg["base-url"]
        selenium.get(base_url)
        sleep(3)
        selenium.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        if instance_cfg["has-cookie-rollbar"]:
            selenium = custom_click_cookie_rollbar(selenium)
        selenium.find_element(By.LINK_TEXT, test_cfg["name"],).click()
        sleep(3)
        assert test_config["external-resources"]["twitter"] == selenium.current_url
