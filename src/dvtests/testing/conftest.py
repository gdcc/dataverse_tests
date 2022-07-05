import os
from json import load
from time import sleep
from typing import Any

import pytest
import requests
from pyDataverse.api import NativeApi
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from dvtests.settings import TestSettings


if os.getenv("ENV_FILE"):
    CONFIG = TestSettings(_env_file=os.getenv("ENV_FILE"))
else:
    CONFIG = TestSettings()
ROOT_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)
DEFAULT_DATAVERSE_CONFIG_DIR = os.path.join(ROOT_DIR, "configs/default", CONFIG.VERSION)
INSTALLATION_TESTING_CONFIG_DIR = os.path.join(
    ROOT_DIR, "configs/installations", CONFIG.INSTANCE, "testing"
)
INSTALLATION_UTILS_CONFIG_DIR = os.path.join(
    ROOT_DIR, "configs/installations", CONFIG.INSTANCE, "utils"
)
TESTDATA_METADATA_JSON_DIR = os.path.join(ROOT_DIR, "dataverse_testdata/metadata/json")
UTILS_DATA_DIR = os.path.join(ROOT_DIR, "data", CONFIG.INSTANCE)


@pytest.fixture()
def config():
    """Get config settings."""
    return CONFIG


@pytest.fixture
def users(config):
    """Load users JSON file."""
    filename = os.path.join(ROOT_DIR, config.USER_FILENAME)
    with open(filename, "r", encoding="utf-8") as f:
        return load(f)


@pytest.fixture
def xpaths():
    """Load XPATH JSON file."""
    filename = os.path.join(DEFAULT_DATAVERSE_CONFIG_DIR, "xpaths.json")
    with open(filename, "r", encoding="utf-8") as f:
        return load(f)


@pytest.fixture
def installation_settings():
    """Load XPATH JSON file."""
    filename = os.path.join(INSTALLATION_TESTING_CONFIG_DIR, "settings.json")
    with open(filename, "r", encoding="utf-8") as f:
        return load(f)


@pytest.fixture
def session(config):
    """Create request session."""
    s = requests.Session()
    s.headers.update({"User-Agent": config.USER_AGENT})
    yield s


@pytest.fixture
def native_api(config):
    """Initialize pyDataverse Native Api object."""
    yield NativeApi(config.BASE_URL)


@pytest.fixture
def firefox_options(firefox_options, config):
    """Set Firefox options."""
    firefox_options.add_argument("-foreground")
    if config.HEADLESS:
        firefox_options.headless = True
    else:
        firefox_options.headless = False
    if config.USER_AGENT:
        firefox_options.set_preference("general.useragent.override", config.USER_AGENT)
    return firefox_options


@pytest.fixture
def chrome_options(chrome_options, config):
    """Set Chrome options."""
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


@pytest.fixture
def homepage(selenium, config, installation_settings):
    """Get homepage with selenium."""
    selenium.get(config.BASE_URL)
    selenium.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    if installation_settings["cookie-rollbar"]:
        custom_click_cookie_rollbar(selenium, config.MAX_WAIT_TIME)
    return selenium


@pytest.fixture
def homepage_logged_in(request, homepage, config, users):
    """Get logged in homepage with selenium."""
    selenium = homepage
    user_handle = request.param
    user_pwd = users[user_handle]["password"]
    user_name = users[user_handle]["firstName"] + " " + users[user_handle]["lastName"]
    user_auth = users[user_handle]["authentication"]
    installation_config = read_json(
        os.path.join(DEFAULT_DATAVERSE_CONFIG_DIR, "xpaths.json")
    )

    wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
    selenium.get(f"{config.BASE_URL}/loginpage.xhtml")
    if "shibboleth" in config.LOGIN_OPTIONS and config.MAX_WAIT_TIME < 15:
        sleep(15)
    else:
        sleep(config.MAX_WAIT_TIME)

    if user_auth == "normal":
        if "shibboleth" in config.LOGIN_OPTIONS:
            btn_login_normal = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, installation_config["login-button-login-normal"])
                )
            )
            btn_login_normal.click()
        input_username_email = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, installation_config["input-username-email"])
            )
        )
        input_username_email.send_keys(user_handle)

        input_pwd = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, installation_config["input-password"])
            )
        )
        input_pwd.send_keys(user_pwd)

        btn_login = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, installation_config["login-button-login"])
            )
        )
        btn_login.click()
        if config.VERSION == "dataverse_5-2" or "dataverse_5-6":
            sleep(3)
            selenium.get(config.BASE_URL)
    elif user_auth == "shibboleth":
        select_institution = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, installation_config["login-institution-select"])
            )
        )
        select_institution.click()

        select_institution.find_element(
            By.XPATH, f"//option[. = '{config.SHIBBOLETH_INSTITUTION}']"
        ).click()

        btn_select_institution = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, installation_config["login-institution-select-button"])
            )
        )
        btn_select_institution.click()

        # Institutions Shibboleth Login Page
        selenium = custom_shibboleth_institution_login(
            selenium, config, user_handle, user_pwd, user_name
        )
    navbar_user = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, installation_config["navbar-user-display-info-title"])
        )
    )
    assert navbar_user.text == user_name
    return homepage, user_handle


def search_navbar(selenium, config, xpaths, query):
    """Search via navbar."""
    wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
    sleep(3)
    navbar_search = wait.until(
        EC.element_to_be_clickable((By.XPATH, xpaths["search-navbar-link"]))
    )
    navbar_search.click()

    navbar_search_input = wait.until(
        EC.element_to_be_clickable((By.XPATH, xpaths["search-navbar-input"]))
    )
    navbar_search_input.clear()
    navbar_search_input.send_keys(query)
    navbar_search_input.send_keys(Keys.ENTER)

    wait.until(
        EC.text_to_be_present_in_element_value(
            (By.XPATH, xpaths["search-sidebar-result"]), "elections"
        )
    )
    return selenium


def search_header(selenium, config, xpaths, query):
    """Search via header."""
    wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
    header_search = wait.until(
        EC.element_to_be_clickable((By.XPATH, xpaths["search-header-input"]))
    )
    header_search.clear()
    header_search.send_keys(query)
    header_search.send_keys(Keys.ENTER)

    wait.until(
        EC.text_to_be_present_in_element_value(
            (By.XPATH, xpaths["search-sidebar-result"]), "elections"
        )
    )
    return selenium


def custom_shibboleth_institution_login(
    selenium, config, user_handle, user_pwd, user_name
):
    """Custom Login on Shibboleth institution page."""
    wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
    input_user_id = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='userid']"))
    )
    print(user_handle)
    print(user_pwd)
    input_user_id.send_keys(user_handle)

    input_user_pwd = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='password']"))
    )
    input_user_pwd.send_keys(user_pwd)
    btn_login = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@name='_eventId_proceed']"))
    )
    btn_login.click()
    sleep(3)

    if selenium.title == config.SHIBBOLETH_LOGIN_PAGE_TITLE:
        btn_tou = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@id='_shib_idp_accept_TOU']")
            )
        )
        btn_tou.click()

        btn_next = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='_eventId_proceed']"))
        )
        btn_next.click()
    navbar_user = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[@id='userDisplayInfoTitle']"))
    )
    assert navbar_user.text == user_name
    return selenium


def custom_click_cookie_rollbar(selenium, max_wait_time):
    """Remove cookie rollbar."""
    wait = WebDriverWait(selenium, max_wait_time)
    sleep(3)
    btn_cookie_accept = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//a[@id='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection']",
            )
        )
    )
    btn_cookie_accept.click()
    return selenium


def read_json(filename: str, mode: str = "r", encoding: str = "utf-8") -> Any:
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


def read_file(filename, mode="r", encoding="utf-8"):
    """Read in a file.

    Parameters
    ----------
    filename : str
        Filename with full path.
    mode : str
        Read mode of file. Defaults to `r`. See more at
        https://docs.python.org/3.5/library/functions.html#open

    Returns
    -------
    str
        Returns data as string.

    """
    with open(filename, mode, encoding=encoding) as f:
        return f.read()


@pytest.fixture
def testdata(request):
    return read_json(os.path.join(TESTDATA_METADATA_JSON_DIR, request.param,))
