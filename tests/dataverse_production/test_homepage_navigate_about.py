import os
import requests
from selenium.webdriver.common.by import By
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))


class TestHomepageNavigateAbout:
    def test_homepage_navigate_about(self, browsers):
        data = read_json(os.path.join(dir_path, "data.json"))

        for driver in browsers:
            driver.get(os.getenv("BASE_URL"))
            driver.set_window_size(1346, 1197)
            vars = {}
            vars["window_handles"] = driver.window_handles
            driver.find_element(By.LINK_TEXT, "About").click()
            vars["root"] = driver.current_window_handle
            vars["website"] = driver.window_handles[1]
            driver.switch_to.window(vars["website"])
            assert driver.current_url == data["website"]["url"]
