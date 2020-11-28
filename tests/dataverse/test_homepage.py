import os
import requests
from time import sleep
from selenium.webdriver.common.by import By
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(os.path.dirname(dir_path), "data")


class TestHomepage:
    def test_homepage_click_about(self, browsers):
        INSTANCE = os.getenv("INSTANCE")
        data = read_json(
            os.path.join(data_path, f"instances/{INSTANCE}/test-data.json")
        )
        base_url = data["instance"]["base-url"]

        for driver in browsers:
            driver.get(base_url)
            driver.set_window_size(1346, 1197)
            vars = {}
            vars["window_handles"] = driver.window_handles
            driver.find_element(By.LINK_TEXT, "About").click()
            vars["root"] = driver.current_window_handle
            print(driver.window_handles)
            vars["website"] = driver.window_handles[1]
            driver.switch_to.window(vars["website"])
            sleep(3)
            assert driver.current_url == data["instance"]["about-url"]

    def test_homepage_click_privacy_policy(self, browsers):
        INSTANCE = os.getenv("INSTANCE")
        data = read_json(
            os.path.join(data_path, f"instances/{INSTANCE}/test-data.json")
        )
        base_url = data["instance"]["base-url"]

        if data["tests"]["footer-privacy-policy-click"]:

            for driver in browsers:
                driver.get(base_url)
                driver.set_window_size(1346, 1197)
                sleep(5)
                if INSTANCE == "dataverse_production":
                    driver.find_element(
                        By.ID,
                        "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection",
                    ).click()
                    sleep(3)
                    driver.find_element(
                        By.LINK_TEXT,
                        data["instance"]["footer"]["privacy-policy"]["name"],
                    ).click()
                    sleep(3)
                assert (
                    data["instance"]["footer"]["privacy-policy"]["url"]
                    == driver.current_url
                )

    def test_homepage_click_contact(self, browsers):
        INSTANCE = os.getenv("INSTANCE")
        data = read_json(
            os.path.join(data_path, f"instances/{INSTANCE}/test-data.json")
        )
        base_url = data["instance"]["base-url"]

        for driver in browsers:
            driver.get(base_url)
            driver.set_window_size(1346, 1197)
            driver.find_element(By.CLASS_NAME, "btn-contact").click()

    def test_homepage_click_branding(self, browsers):
        INSTANCE = os.getenv("INSTANCE")
        data = read_json(
            os.path.join(data_path, f"instances/{INSTANCE}/test-data.json")
        )
        base_url = data["instance"]["base-url"]

        for driver in browsers:
            driver.get(base_url)
            driver.set_window_size(1346, 1197)
            driver.find_element(By.CSS_SELECTOR, ".navbar-header .navbar-brand").click()
            assert data["instance"]["title"] in driver.title
            assert driver.current_url == base_url + "/"

    def test_sidebar_metrics(self, browsers):
        INSTANCE = os.getenv("INSTANCE")
        data = read_json(
            os.path.join(data_path, f"instances/{INSTANCE}/test-data.json")
        )

        if (
            data["tests"]["all-dataverses"]
            or data["tests"]["all-datasets"]
            or data["tests"]["all-datafiles"]
        ):
            metadata = read_json(
                os.path.join(data_path, f"instances/{INSTANCE}/metadata.json")
            )

            base_url = data["instance"]["base-url"]

            for driver in browsers:
                driver.get(base_url)
                driver.set_window_size(1346, 1197)

                if data["tests"]["all-dataverses"]:
                    facet_dataverse = driver.find_element(
                        By.CLASS_NAME, "facetTypeDataverse"
                    )
                    assert (
                        facet_dataverse.text == f"Dataverses ({metadata['dataverses']})"
                    )

                if data["tests"]["all-datasets"]:
                    facet_dataset = driver.find_element(
                        By.CLASS_NAME, "facetTypeDataset"
                    )
                    assert facet_dataset.text == f"Datasets ({metadata['datasets']})"

                if data["tests"]["all-datafiles"]:
                    facet_datafile = driver.find_element(By.CLASS_NAME, "facetTypeFile")
                    assert facet_datafile.text == f"Files ({metadata['datafiles']})"
