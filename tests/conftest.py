from json import load
import os
from time import sleep
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from .config import get_config_name, get_config


@pytest.fixture
def config():
    return get_config(get_config_name())


@pytest.fixture
def firefox(config):
    options = webdriver.firefox.options.Options()
    if config.HEADLESS:
        options.headless = True
    else:
        options.headless = False
    driver = webdriver.Firefox(options=options)
    yield driver
    driver.close()
    driver.quit()


@pytest.fixture
def chrome(config):
    options = webdriver.ChromeOptions()
    if config.HEADLESS:
        options.headless = True
    else:
        options.headless = False
    options.add_argument("--no-sandbox")  # This make Chromium reachable
    options.add_argument("--no-default-browser-check")  # Overrides default choices
    options.add_argument("--no-first-run")
    options.add_argument("--disable-default-apps")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.close()
    driver.quit()


@pytest.fixture
def browsers(config, firefox, chrome):
    browsers = {}
    for browser in config.BROWSERS:
        if browser == "firefox":
            browsers["firefox"] = firefox
        elif browser == "chrome":
            browsers["chrome"] = chrome
    return browsers


@pytest.fixture
def instance(config):
    return config.INSTANCE


@pytest.fixture
def test_data(config):
    return read_json(os.path.join(config.DATA_DIR, "test-data.json"))


def login_normal_user(driver, test_data, config, user, password):
    base_url = test_data["instance"]["base-url"]
    driver.get(f"{base_url}/loginpage.xhtml")
    driver.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    sleep(5)
    driver.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    sleep(10)
    if test_data["tests"]["login"]["login-page"] == "normal-user-and-shibboleth":
        driver.find_element(By.LINK_TEXT, "Username/Email").click()
        sleep(3)
    driver.find_element(By.ID, "loginForm:credentialsContainer:0:credValue").send_keys(
        config.TEST_USER_NORMAL
    )
    driver.find_element(By.ID, "loginForm:credentialsContainer:1:sCredValue").send_keys(
        config.TEST_USER_NORMAL_PWD
    )
    driver.find_element(By.ID, "loginForm:login").click()
    sleep(5)
    return driver


def click_cookie_rollbar(driver):
    driver.find_element(
        By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection"
    ).click()
    sleep(3)


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
        data = load(f)

    return data
