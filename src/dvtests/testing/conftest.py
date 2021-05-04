import os
from json import load

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
DATA_DIR = os.path.join(
    ROOT_DIR, "src/dvtests/data", CONFIG.INSTANCE, CONFIG.DATA_COLLECTOR
)
TESTING_DATA_DIR = os.path.join(ROOT_DIR, "src/dvtests/testing/data", CONFIG.INSTANCE)
TESTDATA_METADATA_DIR = os.path.join(ROOT_DIR, "dataverse_testdata/metadata/json")


@pytest.fixture()
def config():
    return CONFIG


@pytest.fixture
def users(config):
    filename = os.path.join(ROOT_DIR, config.USER_FILENAME)
    with open(filename, "r", encoding="utf-8") as f:
        return load(f)


@pytest.fixture
def session(config):
    s = requests.Session()
    s.headers.update({"User-Agent": config.USER_AGENT})
    yield s


@pytest.fixture
def native_api(config):
    yield NativeApi(config.BASE_URL)


@pytest.fixture
def firefox_options(firefox_options, config):
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
def selenium(selenium, config):
    selenium.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    yield selenium
    selenium.close()
    selenium.quit()


@pytest.fixture
def login_normal(
    selenium, base_url, login_options, user_handle, user_pwd, max_wait_time
):
    """Login with normal user."""
    wait = WebDriverWait(selenium, max_wait_time)
    # set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    selenium.get(f"{base_url}/loginpage.xhtml")

    if "shibboleth" in login_options:
        btn_username_email = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Username/Email"))
        )
        btn_username_email.click()

    input_username_email = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "loginForm:credentialsContainer:0:credValue")
        )
    )
    input_username_email.send_keys(user_handle)

    input_pwd = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "loginForm:credentialsContainer:1:sCredValue")
        )
    )
    input_pwd.send_keys(user_pwd)

    btn_login = wait.until(EC.element_to_be_clickable((By.ID, "loginForm:login")))
    btn_login.click()
    wait.until(EC.element_to_be_clickable((By.ID, "userDisplayInfoTitle")))
    return selenium
    # TODO: logout


def login_shibboleth(
    selenium, config, shibb_login_page_title, user_handle, user_pwd, user_name
):
    """Login with Shibboleth user."""
    wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
    # set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    selenium.get(f"{config.BASE_URL}/loginpage.xhtml")

    if "shibboleth" in config.LOGIN_OPTIONS:
        btn_username_email = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Username/Email"))
        )
        btn_username_email.click()

    select_institution = wait.until(
        EC.element_to_be_clickable((By.ID, "idpSelectSelector"))
    )
    select_institution.click()

    select_institution.find_element(
        By.XPATH, f"//option[. = '{config.SHIBBOLETH_INSTITUTION}']"
    ).click()

    btn_select_institution = wait.until(
        EC.element_to_be_clickable((By.ID, "idpSelectListButton"))
    )
    btn_select_institution.click()

    # Institutions Shibboleth Login Page
    selenium = custom_login_shibboleth_institution_page(
        selenium, config, shibb_login_page_title, user_handle, user_pwd, user_name
    )
    wait.until(EC.element_to_be_clickable((By.ID, "userDisplayInfoTitle")))
    return selenium


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

    wait.until(EC.visibility_of_element_located((By.ID, "dv-main")))
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

    wait.until(EC.visibility_of_element_located((By.ID, "dv-main")))
    return selenium


def custom_login_shibboleth_institution_page(
    selenium, config, shibb_login_page_title, user_handle, user_pwd, user_name
):
    """Login on Shibboleth institution login page."""
    wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
    input_user_id = wait.until(EC.element_to_be_clickable((By.ID, "userid")))
    input_user_id.send_keys(user_handle)

    input_user_pwd = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    input_user_pwd.send_keys(user_pwd)
    btn_login = wait.until(EC.element_to_be_clickable((By.NAME, "_eventId_proceed")))
    btn_login.click()

    if selenium.title == config.SHIBBOLETH_LOGIN_PAGE_TITLE:
        btn_tou = wait.until(
            EC.element_to_be_clickable((By.ID, "_shib_idp_accept_TOU"))
        )
        btn_tou.click()

        btn_next = wait.until(EC.element_to_be_clickable((By.ID, "_eventId_proceed")))
        btn_next.click()
    return selenium


def custom_click_cookie_rollbar(selenium, config):
    """Accept cookie rollbar."""
    wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
    btn_cookie_rollbar = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection")
        )
    )
    btn_cookie_rollbar.click()
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
