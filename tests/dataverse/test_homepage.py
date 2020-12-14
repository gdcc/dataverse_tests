import os
from time import sleep

import pytest
import requests
from selenium.webdriver.common.by import By

from ..conftest import click_cookie_rollbar, read_json


class TestHomepage:
    def test_homepage_click_contact(self, test_config, config, browser):
        if not test_config["tests"]["homepage"]["header-contact-link"]["test"]:
            pytest.skip("Test not configured to be executed.")

        base_url = test_config["instance"]["base-url"]

        for name, driver in browser.items():
            driver.get(base_url)
            sleep(3)
            driver.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
            driver.find_element(By.CLASS_NAME, "btn-contact").click()
            sleep(3)

    def test_homepage_click_branding(self, test_config, config, browser):
        if not test_config["tests"]["homepage"]["header-branding"]["test"]:
            pytest.skip("Test not configured to be executed.")

        base_url = test_config["instance"]["base-url"]

        for name, driver in browser.items():
            driver.get(base_url)
            sleep(3)
            driver.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
            driver.find_element(By.CSS_SELECTOR, ".navbar-header .navbar-brand").click()
            sleep(3)
            assert test_config["instance"]["title"] in driver.title
            assert (
                driver.current_url
                == test_config["tests"]["homepage"]["header-branding"]["url"]
            )

    def test_sidebar_metrics(self, test_config, config, browser):
        if not test_config["tests"]["homepage"]["sidebar-metrics"]["test"]:
            pytest.skip("Test not configured to be executed.")

        base_url = test_config["instance"]["base-url"]
        metadata = read_json(os.path.join(config.INSTANCE_DATA_DIR, "metadata.json"))

        for name, driver in browser.items():
            driver.get(base_url)
            sleep(3)
            driver.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

            if test_config["tests"]["all-dataverses"]:
                facet_dataverse = driver.find_element(
                    By.CLASS_NAME, "facetTypeDataverse"
                )
                assert facet_dataverse.text == f"Dataverses ({metadata['dataverses']})"

            if test_config["tests"]["all-datasets"]:
                facet_dataset = driver.find_element(By.CLASS_NAME, "facetTypeDataset")
                assert facet_dataset.text == f"Datasets ({metadata['datasets']})"

            if test_config["tests"]["all-datafiles"]:
                facet_datafile = driver.find_element(By.CLASS_NAME, "facetTypeFile")
                assert facet_datafile.text == f"Files ({metadata['datafiles']})"


class TestCustomizedHomepage:
    def test_homepage_click_about(self, config, test_config, browser):
        if test_config["tests"]["homepage"]["header-about"]["test"]:
            pytest.skip("Test not configured to be executed.")

        base_url = test_config["instance"]["base-url"]

        for name, driver in browser.items():
            driver.get(base_url)
            sleep(3)
            driver.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
            vars = {}
            vars["window_handles"] = driver.window_handles
            driver.find_element(By.LINK_TEXT, "About").click()
            sleep(3)
            vars["root"] = driver.current_window_handle
            print(driver.window_handles)
            vars["website"] = driver.window_handles[1]
            driver.switch_to.window(vars["website"])
            sleep(3)
            assert (
                driver.current_url
                == test_config["tests"]["homepage"]["header-about"]["url"]
            )

    def test_homepage_click_privacy_policy(self, test_config, config, browser):
        if not test_config["tests"]["homepage"]["footer-privacy-policy"]["test"]:
            pytest.skip("Test not configured to be executed.")

        base_url = test_config["instance"]["base-url"]
        for name, driver in browser.items():
            driver.get(base_url)
            sleep(3)
            driver.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
            if test_config["instance"]["has-cookie-rollbar"]:
                driver = click_cookie_rollbar(driver)
                driver.find_element(
                    By.LINK_TEXT,
                    test_config["tests"]["homepage"]["footer-privacy-policy"]["name"],
                ).click()
                sleep(3)
            assert (
                test_config["tests"]["homepage"]["footer-privacy-policy"]["url"]
                == driver.current_url
            )
