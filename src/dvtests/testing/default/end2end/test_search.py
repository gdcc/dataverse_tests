from time import sleep

import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestSearch:
    @pytest.mark.v4_18_1
    @pytest.mark.selenium
    def test_search_header(self, test_config, selenium):
        """

        Input
        * base url
        * query term
        * search option: top, side

        Expected result
        * num dataverses
        * num datasets
        * num datafiles

        """
        instance_cfg = test_config["instance"]

        base_url = instance_cfg["base-url"]

        for search in test_config["search"]:
            selenium.get(base_url)
            sleep(3)
            selenium.set_window_size(1346, 1197)
            selenium.find_element(By.LINK_TEXT, "Search").click()
            sleep(3)
            search_navbar = selenium.find_element(By.ID, "navbarsearch")
            search_navbar.clear()
            search_navbar.send_keys(search["query-text"])
            search_navbar.send_keys(Keys.ENTER)
            sleep(3)
            assert selenium.current_url == search["result-url"]

            num_dataverses = search["found-dataverses"]
            num_datasets = search["found-datasets"]
            num_datafiles = search["found-datafiles"]

            facet_dataverse = selenium.find_element(By.CLASS_NAME, "facetTypeDataverse")
            assert facet_dataverse.text == f"Dataverses ({num_dataverses})"

            facet_dataset = selenium.find_element(By.CLASS_NAME, "facetTypeDataset")
            assert facet_dataset.text == f"Datasets ({num_datasets})"

            facet_datafile = selenium.find_element(By.CLASS_NAME, "facetTypeFile")
            assert facet_datafile.text == f"Files ({num_datafiles})"
