import requests
import os
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(os.path.dirname(dir_path), "data")


class TestSearch:
    def test_search_header(self, browsers):
        INSTANCE = os.getenv("INSTANCE")
        data = read_json(os.path.join(data_path, f"instance/dataverse_{INSTANCE}.json"))
        base_url = data["instances"][INSTANCE]["base-url"]

        for driver in browsers:
            for search in data["search"]:
                driver.get(base_url)
                driver.set_window_size(1346, 1197)
                driver.find_element(By.LINK_TEXT, "Search").click()
                driver.find_element(By.ID, "navbarsearch").send_keys(search["query"])
                driver.find_element(By.ID, "navbarsearch").send_keys(Keys.ENTER)
                sleep(3)
                assert driver.current_url == search["result-url"]
