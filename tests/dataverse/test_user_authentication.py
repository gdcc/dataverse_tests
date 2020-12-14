from time import sleep

import pytest
import requests
from selenium.webdriver.common.by import By

from ..conftest import login_normal_user, login_shibboleth_user


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
                driver, test_config, config, config.USER_NORMAL, config.USER_NORMAL_PWD,
            )
            assert test_config["instance"]["title"] == driver.title
            assert (
                driver.find_element(By.ID, "userDisplayInfoTitle").text
                == config.USER_NORMAL_NAME
            )

    def test_login_shibboleth_user(self, test_config, config, browser):
        if not test_config["tests"]["login"]["shibboleth-user"]["test"]:
            pytest.skip("Test not configured to be executed.")

        for name, driver in browser.items():
            driver = login_shibboleth_user(
                driver,
                test_config,
                config,
                config.USER_SHIBBOLETH,
                config.USER_SHIBBOLETH_PWD,
            )
            assert test_config["instance"]["title"] == driver.title
            assert (
                driver.find_element(By.ID, "userDisplayInfoTitle").text
                == config.USER_SHIBBOLETH_NAME
            )
        assert 0
