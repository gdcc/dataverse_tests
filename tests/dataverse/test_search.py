import requests
import pytest
import os
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class TestSearch:
    def test_search_header(self, test_config, browser):
        if not test_config["tests"]["search"]["test"]:
            pytest.skip("Test not configured to be executed.")

        base_url = test_config["instance"]["base-url"]

        for name, driver in browser.items():
            for search in test_config["search"]:
                driver.get(base_url)
                sleep(3)
                driver.set_window_size(1346, 1197)
                driver.find_element(By.LINK_TEXT, "Search").click()
                sleep(3)
                driver.find_element(By.ID, "navbarsearch").send_keys(search["query"])
                driver.find_element(By.ID, "navbarsearch").send_keys(Keys.ENTER)
                sleep(3)
                assert driver.current_url == search["result-url"]

                num_dataverses = search["found-dataverses"]
                num_datasets = search["found-datasets"]
                num_datafiles = search["found-datafiles"]

                facet_dataverse = driver.find_element(
                    By.CLASS_NAME, "facetTypeDataverse"
                )
                assert facet_dataverse.text == f"Dataverses ({num_dataverses})"

                facet_dataset = driver.find_element(By.CLASS_NAME, "facetTypeDataset")
                assert facet_dataset.text == f"Datasets ({num_datasets})"

                facet_datafile = driver.find_element(By.CLASS_NAME, "facetTypeFile")
                assert facet_datafile.text == f"Files ({num_datafiles})"
