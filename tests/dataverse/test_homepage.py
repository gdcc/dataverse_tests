import os
import requests
from time import sleep
from selenium.webdriver.common.by import By
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))


class TestHomepage:
    def test_homepage_click_about(self, browsers):
        data = read_json(os.path.join(dir_path, "data.json"))

        for driver in browsers:
            driver.get(os.getenv("BASE_URL"))
            driver.set_window_size(1346, 1197)
            vars = {}
            vars["window_handles"] = driver.window_handles
            driver.find_element(By.LINK_TEXT, "About").click()
            vars["root"] = driver.current_window_handle
            print(driver.window_handles)
            vars["website"] = driver.window_handles[1]
            driver.switch_to.window(vars["website"])
            sleep(3)
            assert driver.current_url == data["website"]["url"]

    def test_homepage_click_privacy_policy(self, browsers):
        data = read_json(os.path.join(dir_path, "data.json"))

        for driver in browsers:
            driver.get(os.getenv("BASE_URL"))
            driver.set_window_size(1346, 1197)
            sleep(5)
            driver.find_element(
                By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection"
            ).click()
            sleep(3)
            driver.find_element(By.LINK_TEXT, "Privacy Policy").click()
            sleep(3)
            assert data["website"]["privacy-policy"]["en"]["url"] == driver.current_url
            assert data["website"]["privacy-policy"]["en"]["title"] == driver.title

    def test_homepage_click_contact(self, browsers):
        for driver in browsers:
            driver.get(os.getenv("BASE_URL"))
            driver.set_window_size(1346, 1197)
            driver.find_element(By.CLASS_NAME, "btn-contact").click()
            # TODO: Test pop-up form

    def test_homepage_click_branding(self, browsers):
        for driver in browsers:
            url = os.getenv("BASE_URL")
            driver.get(url)
            driver.set_window_size(1346, 1197)
            driver.find_element(By.CSS_SELECTOR, ".navbar-header .navbar-brand").click()
            assert "AUSSDA" in driver.title
            assert driver.current_url == url
