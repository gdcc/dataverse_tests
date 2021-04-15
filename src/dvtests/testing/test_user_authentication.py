from time import sleep

import pytest
import requests
from selenium.webdriver.common.by import By

from ..conftest import login_normal_user
from ..conftest import login_shibboleth_user


class TestShibboleth:
    def test_interfaces(self, test_config):
        test_cfg = test_config["tests"]["login"]["shibboleth-endpoint"]
        instance_cfg = test_config["instance"]

        if not test_cfg:
            pytest.skip("Test not configured to be executed.")

        base_url = instance_cfg["base-url"]
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

    def test_login(self, test_config, config, browser):
        test_cfg = test_config["tests"]["login"]["shibboleth-user"]
        instance_cfg = test_config["instance"]

        if not test_cfg["test"]:
            pytest.skip("Test not configured to be executed.")

        for name, driver in browser.items():
            driver = login_shibboleth_user(
                driver,
                test_cfg["base-url"],
                config.WINDOW_WIDTH,
                config.WINDOW_,
                config.USER_SHIBBOLETH,
                config.USER_SHIBBOLETH_PWD,
                config.USER_SHIBBOLETH_NAME,
            )
            assert instance_cfg["title"] == driver.title
            assert (
                driver.find_element(By.ID, "userDisplayInfoTitle").text
                == config.USER_SHIBBOLETH_NAME
            )


class TestNormalLogin:
    def test_login(self, test_config, config, browser):
        test_cfg = test_config["tests"]["login"]["normal-user"]
        instance_cfg = test_config["instance"]

        if not test_cfg["test"]:
            pytest.skip("Test not configured to be executed.")

        for name, driver in browser.items():
            driver = login_normal_user(
                driver, test_config, config, config.USER_NORMAL, config.USER_NORMAL_PWD,
            )
            assert instance_cfg["title"] == driver.title
            assert (
                driver.find_element(By.ID, "userDisplayInfoTitle").text
                == config.USER_NORMAL_NAME
            )
