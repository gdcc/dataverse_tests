import os
from time import sleep
from selenium.webdriver.common.by import By
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(os.path.dirname(dir_path), "data")


class UserProfile:
    def test_user_profile_navigate(self, browsers):
        INSTANCE = os.getenv("INSTANCE")
        data = read_json(
            os.path.join(data_path, f"instances/{INSTANCE}/test-data.json")
        )
        base_url = data["instance"]["base-url"]

        for driver in browsers:
            driver.get(base_url)
            driver.set_window_size(1346, 1197)
            driver.find_element(By.LINK_TEXT, "Log In").click()
            driver.find_element(
                By.ID, "loginForm:credentialsContainer:0:credValue"
            ).send_keys("TestUser_NormalLogin")
            driver.find_element(
                By.ID, "loginForm:credentialsContainer:1:sCredValue"
            ).send_keys('Q9u/k_v=t9]q=)%bG.e"5Q')
            driver.find_element(By.CSS_SELECTOR, ".ui-button-text").click()
            sleep(2)
            assert data["instance"]["title"] in driver.title
            driver.find_element(By.ID, "userDisplayInfoTitle").click()
            driver.find_element(By.LINK_TEXT, "My Data").click()
            assert f"Account - {data['instance']['title']}" in driver.title
            driver.find_element(By.LINK_TEXT, "Notifications").click()
            driver.find_element(By.LINK_TEXT, "Account Information").click()
            driver.find_element(By.LINK_TEXT, "API Token").click()
