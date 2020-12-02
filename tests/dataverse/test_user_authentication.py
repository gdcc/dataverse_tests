import os
import pytest
import requests
from time import sleep
from selenium.webdriver.common.by import By
from ..conftest import login_normal_user


class TestUserAuthentication:
    def test_shibboleth_interfaces(self, test_config):
        if not test_config["tests"]["login"]["shibboleth-endpoint"]["test"]:
            pytest.skip("Test not configured to be executed.")

        base_url = test_config["instance"]["base-url"]
        url = f"{base_url}/Shibboleth.sso/DiscoFeed"
        resp = requests.get(url)
        sleep(3)
        assert resp.status_code == 200
        assert resp.url == url
        assert resp.encoding == "UTF-8"
        assert "application/json" in requests.head(url).headers["Content-Type"]

        url = f"{base_url}/Shibboleth.sso/Metadata"
        resp = requests.get(url)
        sleep(3)
        assert resp.status_code == 200
        assert resp.url == url

    def test_login_normal_user(self, test_config, config, browser):
        if not test_config["tests"]["login"]["normal-user"]["test"]:
            pytest.skip("Test not configured to be executed.")

        for name, driver in browser.items():
            driver = login_normal_user(
                driver,
                test_config,
                config,
                config.TEST_USER_NORMAL,
                config.TEST_USER_NORMAL_PWD,
            )
            assert test_config["instance"]["title"] == driver.title
            assert (
                driver.find_element(By.ID, "userDisplayInfoTitle").text
                == config.TEST_USER_NORMAL_NAME
            )
