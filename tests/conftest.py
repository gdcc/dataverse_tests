from json import load
import os
from time import sleep
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from .config import Config


@pytest.fixture
def config():
    if os.getenv("ENV_FILE"):
        return Config(_env_file=os.getenv("ENV_FILE"))
    else:
        return Config()


@pytest.fixture
def firefox(config):
    options = webdriver.firefox.options.Options()
    if config.HEADLESS:
        options.headless = True
    else:
        options.headless = False
    profile = webdriver.FirefoxProfile()
    if config.USER_AGENT:
        profile.set_preference("general.useragent.override", "SELENIUM-TEST")
    driver = webdriver.Firefox(firefox_profile=profile, options=options)
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
    if config.USER_AGENT:
        options.add_argument(f"user-agent={config.USER_AGENT}")
    options.add_argument("--no-sandbox")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.close()
    driver.quit()


@pytest.fixture
def browser(config, firefox, chrome):
    browser = {}
    for b in config.BROWSER:
        if b == "firefox":
            browser["firefox"] = firefox
        elif b == "chrome":
            browser["chrome"] = chrome
    return browser


@pytest.fixture
def test_config(config):
    instance_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "data/instances", config.INSTANCE
    )
    return read_json(os.path.join(instance_dir, config.TEST_CONFIG_FILENAME))


def get_instance_dir(config):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "data/instances", config.INSTANCE
    )


def login_normal_user(driver, test_config, config, user, password):
    base_url = test_config["instance"]["base-url"]
    driver.get(f"{base_url}/loginpage.xhtml")
    driver.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    sleep(5)
    if test_config["tests"]["login"]["login-page"] == "normal-user-and-shibboleth":
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


def login_shibboleth_user(driver, test_config, config, user, password):
    base_url = test_config["instance"]["base-url"]
    driver.get(f"{base_url}/loginpage.xhtml")
    sleep(5)
    driver.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    sleep(5)
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
        data = load(f)

    return data
