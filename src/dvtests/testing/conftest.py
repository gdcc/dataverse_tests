import os
from json import load
from time import sleep

import pytest
import requests
from pyDataverse.api import NativeApi
from selenium import webdriver
from selenium.webdriver.common.by import By

from dvtests.config import TestingConfig


ROOT_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)


@pytest.fixture
def config():
    # Arrange
    # Act
    # Assert
    # Cleanup
    if os.getenv("ENV_FILE"):
        return TestingConfig(_env_file=os.getenv("ENV_FILE"))
    else:
        return TestingConfig()


INSTANCE = (
    TestingConfig(_env_file=os.getenv("ENV_FILE")).INSTANCE
    if os.getenv("ENV_FILE")
    else TestingConfig().INSTANCE
)
BASE_URL = (
    TestingConfig(_env_file=os.getenv("ENV_FILE")).BASE_URL
    if os.getenv("ENV_FILE")
    else TestingConfig().BASE_URL
)


@pytest.fixture
def session(config):
    # Arrange
    # Act
    # Assert
    # Cleanup
    s = requests.Session()
    s.headers.update({"User-Agent": config.USER_AGENT})
    return s


@pytest.fixture
def native_api(config):
    # Arrange
    # Act
    # Assert
    # Cleanup
    return NativeApi(BASE_URL)


@pytest.fixture
def test_config(config):
    # Arrange
    # Act
    # Assert
    # Cleanup
    instance_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
    return read_json(os.path.join(instance_dir, config.INSTANCE + ".json"))


@pytest.fixture
def firefox_options(firefox_options, config):
    # Arrange
    # Act
    # Assert
    # Cleanup
    firefox_options.add_argument("-foreground")
    if config.HEADLESS:
        firefox_options.headless = True
    else:
        firefox_options.headless = False
    if config.USER_AGENT:
        firefox_options.set_preference("general.useragent.override", "SELENIUM-TEST")
    return firefox_options


@pytest.fixture
def chrome_options(chrome_options, config):
    # Arrange
    # Act
    # Assert
    # Cleanup
    if config.HEADLESS:
        chrome_options.add_argument("--headless")
    if config.USER_AGENT:
        chrome_options.add_argument(f"user-agent={config.USER_AGENT}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return chrome_options


def login_normal_user(driver, login_mode, window_width, window_height, user, password):
    driver.get(f"{BASE_URL}/loginpage.xhtml")
    driver.set_window_size(window_width, window_height)
    sleep(5)
    if login_mode == "normal-user-and-shibboleth":
        driver.find_element(By.LINK_TEXT, "Username/Email").click()
        sleep(3)
    driver.find_element(By.ID, "loginForm:credentialsContainer:0:credValue").send_keys(
        user
    )
    driver.find_element(By.ID, "loginForm:credentialsContainer:1:sCredValue").send_keys(
        password
    )
    driver.find_element(By.ID, "loginForm:login").click()
    sleep(5)
    return driver


def login_shibboleth_user(driver, base_url, width, height, user, password, name):
    driver.get(f"{base_url}/loginpage.xhtml")
    sleep(5)
    driver.set_window_size(width, height)
    sleep(10)
    driver.find_element(By.ID, "idpSelectSelector").click()
    sleep(1)
    dropdown = driver.find_element(By.ID, "idpSelectSelector")
    dropdown.find_element(By.XPATH, "//option[. = 'University of Vienna']").click()
    sleep(1)
    driver.find_element(By.ID, "idpSelectListButton").click()
    sleep(1)
    driver.find_element(By.ID, "userid").click()
    driver.find_element(By.ID, "userid").send_keys(user)
    driver.find_element(By.ID, "password").click()
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.NAME, "_eventId_proceed").click()
    sleep(3)
    if driver.title == "Weblogin | Universität Wien":
        driver.find_element(By.ID, "_shib_idp_accept_TOU").click()
        driver.find_element(By.NAME, "_eventId_proceed").click()
        sleep(5)
    assert driver.find_element(By.ID, "userDisplayInfoTitle").text == name
    return driver


def click_cookie_rollbar(driver):
    driver.find_element(
        By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection"
    ).click()
    sleep(3)
    return driver


def read_json(filename: str, mode: str = "r", encoding: str = "utf-8") -> dict:
    """Read in a json file.

    See more about the json module at
    https://docs.python.org/3.5/library/json.html

    Parameters
    ----------
    filename : str
        Filename with full path.
    mode : str
        Read mode of file. Defaults to `w`. See more at
        https://docs.python.org/3.5/library/functions.html#open
    encoding : str
        Character encoding of file. Defaults to 'utf-8'.

    Returns
    -------
    dict
        Data as a json-formatted string.

    """
    with open(filename, mode, encoding=encoding) as f:
        return load(f)


@pytest.fixture
def dataverse_upload_full_01():
    # Arrange
    # Act
    # Assert
    # Cleanup
    return read_json(
        os.path.join(
            ROOT_DIR,
            "dataverse_testdata/metadata/json/dataverse/dataverse_upload_full_01.json",
        )
    )


@pytest.fixture
def dataverse_upload_min_01():
    # Arrange
    # Act
    # Assert
    # Cleanup
    return read_json(
        os.path.join(
            ROOT_DIR,
            "dataverse_testdata/metadata/json/dataverse/dataverse_upload_min_01.json",
        )
    )


@pytest.fixture
def dataset_upload_default_full_01():
    # Arrange
    # Act
    # Assert
    # Cleanup
    return read_json(
        os.path.join(
            ROOT_DIR,
            "dataverse_testdata/metadata/json/dataset/dataset_upload_default_full_01.json",
        )
    )


@pytest.fixture
def dataset_upload_default_min_02():
    # Arrange
    # Act
    # Assert
    # Cleanup
    return read_json(
        os.path.join(
            ROOT_DIR,
            "dataverse_testdata/metadata/json/dataset/dataset_upload_default_min_01.json",
        )
    )


@pytest.fixture
def datafile_upload_full_01():
    # Arrange
    # Act
    # Assert
    # Cleanup
    return read_json(
        os.path.join(
            ROOT_DIR,
            "dataverse_testdata/metadata/json/datafile/datafile_upload_full_01.json",
        )
    )


@pytest.fixture
def datafile_upload_min_01():
    # Arrange
    # Act
    # Assert
    # Cleanup
    return read_json(
        os.path.join(
            ROOT_DIR,
            "dataverse_testdata/metadata/json/datafile/datafile_upload_min_01.json",
        )
    )
