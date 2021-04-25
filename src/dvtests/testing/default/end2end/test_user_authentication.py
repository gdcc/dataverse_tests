from time import sleep

import pytest
import requests
from selenium.webdriver.common.by import By

from ..conftest import login_normal_user
from ..conftest import login_shibboleth_user


class TestShibboleth:
    @pytest.mark.v4_18_1
    def test_interfaces(self, test_config):
        """

        Input
        * base url

        Expected result
        * status code
        * encoding
        * content type

        """
        instance_cfg = test_config["instance"]

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

    @pytest.mark.v4_18_1
    @pytest.mark.selenium
    def test_login(self, test_config, config, selenium):
        """

        Input
        * base url
        * user(s)

        Expected result
        * user
            * name

        """
        base_url = test_config["instance"]["base-url"]
        instance_cfg = test_config["instance"]

        selenium = login_shibboleth_user(
            selenium,
            base_url,
            config.WINDOW_WIDTH,
            config.WINDOW_HEIGHT,
            config.USER_SHIBBOLETH,
            config.USER_SHIBBOLETH_PWD,
            config.USER_SHIBBOLETH_NAME,
        )
        assert instance_cfg["title"] == selenium.title
        assert (
            selenium.find_element(By.ID, "userDisplayInfoTitle").text
            == config.USER_SHIBBOLETH_NAME
        )


class TestNormalLogin:
    @pytest.mark.v4_18_1
    @pytest.mark.selenium
    def test_login(self, test_config, config, selenium):
        """

        Input
        * base url

        Expected result
        * user
            * name

        """
        instance_cfg = test_config["instance"]

        selenium = login_normal_user(
            selenium, test_config, config, config.USER_NORMAL, config.USER_NORMAL_PWD,
        )
        assert instance_cfg["title"] == selenium.title
        assert (
            selenium.find_element(By.ID, "userDisplayInfoTitle").text
            == config.USER_NORMAL_NAME
        )
