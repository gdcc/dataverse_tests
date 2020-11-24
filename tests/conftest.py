from json import load
import pytest
from selenium import webdriver
from .config import get_config_name, get_config


config = get_config(get_config_name())


@pytest.fixture
def firefox():
    options = webdriver.firefox.options.Options()
    if config.HEADLESS:
        options.headless = True
    else:
        options.headless = False
    driver = webdriver.Firefox(options=options)
    vars = {}
    yield driver
    driver.close()
    driver.quit()


@pytest.fixture
def chrome():
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
    vars = {}
    yield driver
    driver.close()
    driver.quit()


@pytest.fixture
def browser(firefox, chrome):
    for browser in [firefox, chrome]:
        return browser


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
