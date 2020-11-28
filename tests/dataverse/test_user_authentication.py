import os
import requests
from time import sleep
from selenium.webdriver.common.by import By
from ..conftest import login_normal_user


class TestUserAuthentication:
    def test_shibboleth_interfaces(self, test_data):
        if test_data["tests"]["login"]["shibboleth-endpoint"]["test"]:
            base_url = test_data["instance"]["base-url"]
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

    def test_login_normal_user(self, test_data, config, browsers):
        if test_data["tests"]["login"]["normal-user"]["test"]:
            for name, driver in browsers.items():
                driver = login_normal_user(
                    driver,
                    test_data,
                    config,
                    config.TEST_USER_NORMAL,
                    config.TEST_USER_NORMAL_PWD,
                )
                assert test_data["instance"]["title"] == driver.title
                assert (
                    driver.find_element(By.ID, "userDisplayInfoTitle").text
                    == config.TEST_USER_NORMAL_NAME
                )
