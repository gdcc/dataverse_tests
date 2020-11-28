import os
import requests
from time import sleep
from selenium.webdriver.common.by import By
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(os.path.dirname(dir_path), "data")


class TestUserAuthentication:
    def test_shibboleth_interfaces(self):
        INSTANCE = os.getenv("INSTANCE")
        data = read_json(
            os.path.join(data_path, f"instances/{INSTANCE}/test-data.json")
        )
        base_url = data["instance"]["base-url"]

        if data["tests"]["shibboleth"]:
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

    def test_login_normal_user(self, browsers):
        INSTANCE = os.getenv("INSTANCE")
        data = read_json(
            os.path.join(data_path, f"instances/{INSTANCE}/test-data.json")
        )
        base_url = data["instance"]["base-url"]

        if data["tests"]["login-user"]:
            for driver in browsers:
                driver.get(f"{base_url}/loginpage.xhtml")
                driver.set_window_size(1346, 1197)
                assert data["instance"]["title"] in driver.title
                driver.find_element(By.LINK_TEXT, "Log In").click()
                assert data["instance"]["title"] in driver.title
                driver.find_element(
                    By.ID, "loginForm:credentialsContainer:0:credValue"
                ).send_keys("TestUser_NormalLogin")
                driver.find_element(
                    By.ID, "loginForm:credentialsContainer:1:sCredValue"
                ).send_keys('Q9u/k_v=t9]q=)%bG.e"5Q')
                driver.find_element(By.CSS_SELECTOR, ".ui-button-text").click()
                sleep(1)
                assert data["instance"]["title"] in driver.title
                driver.find_element(By.ID, "userDisplayInfoTitle").click()
                driver.find_element(By.LINK_TEXT, "Log Out").click()
                sleep(1)
                assert data["instance"]["title"] in driver.title
