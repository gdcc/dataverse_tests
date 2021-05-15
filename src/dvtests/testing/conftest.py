import os
from json import load
from time import sleep

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
UTILS_DATA_DIR = os.path.join(
    ROOT_DIR, "src/dvtests/data", CONFIG.INSTANCE, CONFIG.DATA_COLLECTOR
)
TEST_CONFIG_DATA_DIR = os.path.join(
    ROOT_DIR, "src/dvtests/testing/data/test_configs", CONFIG.INSTANCE
)
DATAVERSE_VERSION_DIR = os.path.join(
    ROOT_DIR,
    "src/dvtests/testing/data/dataverse_versions",
    CONFIG.VERSION.replace(".", "_"),
)
TESTDATA_METADATA_DIR = os.path.join(ROOT_DIR, "dataverse_testdata/metadata/json")


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
def homepage(selenium, config):
    """Get homepage with selenium."""
    selenium.get(config.BASE_URL)
    selenium.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    custom_click_cookie_rollbar(selenium, config.MAX_WAIT_TIME)
    return selenium


@pytest.fixture
def homepage_logged_in(request, homepage, config, users):
    """Get logged in homepage with selenium."""
    selenium = homepage
    user_handle = request.param
    user_pwd = users[user_handle]["password"]
    user_name = (
        users[user_handle]["given-name"] + " " + users[user_handle]["family-name"]
    )
    user_auth = users[user_handle]["authentication"]

    wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
    selenium.get(f"{config.BASE_URL}/loginpage.xhtml")
    sleep(15)

    if user_auth == "normal":
        btn_username_email = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Username/Email']"))
        )
        btn_username_email.click()
        input_username_email = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@id='loginForm:credentialsContainer:0:credValue']")
            )
        )
        input_username_email.send_keys(user_handle)

        input_pwd = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@id='loginForm:credentialsContainer:1:sCredValue']")
            )
        )
        input_pwd.send_keys(user_pwd)

        btn_login = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='loginForm:login']"))
        )
        btn_login.click()
    elif user_auth == "shibboleth":
        select_institution = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//select[@id='idpSelectSelector']"))
        )
        select_institution.click()

        select_institution.find_element(
            By.XPATH, f"//option[. = '{config.SHIBBOLETH_INSTITUTION}']"
        ).click()

        btn_select_institution = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='idpSelectListButton']"))
        )
        btn_select_institution.click()

        # Institutions Shibboleth Login Page
        selenium = custom_shibboleth_institution_login(
            selenium, config, user_handle, user_pwd, user_name
        )
    navbar_user = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[@id='userDisplayInfoTitle']"))
    )
    assert navbar_user.text == user_name
    return homepage, user_handle


def search_navbar(selenium, config, query):
    """Search via navbar."""
    wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
    selenium.get(config.BASE_URL)
    navbar_search = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Search")))
    navbar_search.click()

    navbar_search_input = wait.until(
        EC.element_to_be_clickable((By.ID, "navbarsearch"))
    )
    navbar_search_input.clear()
    navbar_search_input.send_keys(query)
    navbar_search_input.send_keys(Keys.ENTER)

    wait.until(
        EC.text_to_be_present_in_element_value(
            (By.XPATH, "//input[@id='j_idt421:searchBasic']"), "elections"
        )
    )
    return selenium


def search_header(selenium, config, query):
    """Search via header."""
    wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
    selenium.get(config.BASE_URL)
    header_search = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.search-input"))
    )
    header_search.clear()
    header_search.send_keys(query)
    header_search.send_keys(Keys.ENTER)

    wait.until(
        EC.text_to_be_present_in_element_value(
            (By.XPATH, "//input[@id='j_idt421:searchBasic']"), "elections"
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
        os.path.join(TESTDATA_METADATA_DIR, "dataverse/dataverse_upload_full_01.json",)
    )


@pytest.fixture
def dataverse_upload_min_01():
    # Arrange
    # Act
    # Assert
    # Cleanup
    return read_json(
        os.path.join(TESTDATA_METADATA_DIR, "dataverse/dataverse_upload_min_01.json",)
    )


@pytest.fixture
def dataset_upload_default_full_01():
    # Arrange
    # Act
    # Assert
    # Cleanup
    return read_json(
        os.path.join(
            TESTDATA_METADATA_DIR, "dataset/dataset_upload_default_full_01.json",
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
            TESTDATA_METADATA_DIR, "dataset/dataset_upload_default_min_01.json",
        )
    )


@pytest.fixture
def datafile_upload_full_01():
    # Arrange
    # Act
    # Assert
    # Cleanup
    return read_json(
        os.path.join(TESTDATA_METADATA_DIR, "datafile/datafile_upload_full_01.json",)
    )


@pytest.fixture
def datafile_upload_min_01():
    # Arrange
    # Act
    # Assert
    # Cleanup
    return read_json(
        os.path.join(TESTDATA_METADATA_DIR, "datafile/datafile_upload_min_01.json",)
    )
