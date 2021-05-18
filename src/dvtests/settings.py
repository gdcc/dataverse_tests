import os
import sys
from typing import List

from pydantic import BaseSettings

if os.getenv("ENV_FILE"):
    ENV_FILE_BASE = str(os.path.splitext(os.path.basename(os.getenv("ENV_FILE")))[0])
else:
    sys.exit("ERROR: 'ENV_FILE' missing.")


class UtilsSettings(BaseSettings):
    """Utils settings.

    * `BASE_URL`: Base URL of your Dataverse installation without trailing slash.
    * `USER_FILENAME`: relative path to user file (JSON)
    * `PRODUCTION`: If `true`, the creation and removal of test-data is not activated. This is important to set to `true`, if this represents a production instance, as you don't want to create or delete data on production. To allow creation or removal on a production instance, you have to pass `--force` to the function call.
    * `INSTANCE`: Name for instance. First an institution-specific string (e. g. "aussda"), second an installation-specific one (e. g. "production"). This will also be the folder name, where your test-specific data is stored in (`src/dvtests/testing/data/INSTANCE/`, `src/dvtests/testing/custom/INSTANCE/`)
    * `FILENAME_DATAVERSES`: name of created dataverse JSON file from utils collect
    * `FILENAME_DATASETS`: name of created datasets JSON file from utils collect
    * `FILENAME_DATAFILES`: name of created datafiles JSON file from utils collect
    * `FILENAME_METADATA`: name of created metadata JSON file from utils collect
    * `BUILTIN_USER_KEY`: Builtin user key to create users

    """

    BASE_URL: str
    USER_FILENAME: str
    PRODUCTION: bool = False
    INSTANCE: str = ENV_FILE_BASE
    FILENAME_DATAVERSES: str = "dataverses.json"
    FILENAME_DATASETS: str = "datasets.json"
    FILENAME_DATAFILES: str = "datafiles.json"
    FILENAME_METADATA: str = "metadata.json"
    BUILTIN_USER_KEY: str = None


class TestSettings(BaseSettings):
    """Settings for Testing.

    * `BASE_URL`: Base URL of your Dataverse installation without trailing slash.
    * `USER_FILENAME`: relative path to user file (JSON)
    * `VERSION`: Dataverse version string. e. g. `4.20`
    * `INSTANCE`: Name for instance. First an institution-specific string (e. g. "aussda"), second an installation-specific one (e. g. "production"). This will also be the folder name, where your test-specific data is stored in (`src/dvtests/testing/data/INSTANCE/`, `src/dvtests/testing/custom/INSTANCE/`)
    * `HEADLESS`: Executes Selenium tests with or without browser window opening (default = `true` -> without browser window).
    * `USER_AGENT`: Passed user agent for requests and selenium requests (e. g. `SELENIUM-TEST`). This allows to exclude tracking by your web-analytics tool (e. g. Matomo, Google Analytics) of requests done by Dataverse tests. For this, you have to tell your web-analytics tool to exclude all visits with the defined user-agent.
    * `WINDOW_HEIGHT`: Window height for Selenium
    * `WINDOW_WIDTH`: Window width for Selenium
    * `MAX_WAIT_TIME`: max wait time for selenium waits
    * `LOGIN_OPTIONS`: List of user login options (options: `normal`, `shibboleth`)
    * `FILENAME_DATAVERSES`: name of created dataverse JSON file from utils collect
    * `FILENAME_DATASETS`: name of created datasets JSON file from utils collect
    * `FILENAME_DATAFILES`: name of created datafiles JSON file from utils collect
    * `FILENAME_METADATA`: name of created metadata JSON file from utils collect
    * `SHIBBOLETH_INSTITUTION`: name of Shibboleth institution for login purpose
    * `SHIBBOLETH_LOGIN_PAGE_TITLE`: title of Shibboleth Login page
    * `BUILTIN_USER_KEY`: Builtin user key to create users
    * `DATA_COLLECTOR`: descriptor for data collector. It is ether 1. the user handle of dataverse user, which collected the data or 2. "public" for publicly accessible data

    """

    BASE_URL: str
    USER_FILENAME: str
    VERSION: str
    INSTANCE: str = ENV_FILE_BASE
    HEADLESS: bool = True
    USER_AGENT: str = "TESTING"
    WINDOW_HEIGHT: int = 1400
    WINDOW_WIDTH: int = 1600
    MAX_WAIT_TIME: int = 20
    LOGIN_OPTIONS: List[str] = ["normal"]
    FILENAME_DATAVERSES: str = "dataverses.json"
    FILENAME_DATASETS: str = "datasets.json"
    FILENAME_DATAFILES: str = "datafiles.json"
    FILENAME_METADATA: str = "metadata.json"
    SHIBBOLETH_INSTITUTION: str = None
    SHIBBOLETH_LOGIN_PAGE_TITLE: str = None
    BUILTIN_USER_KEY: str = None
    DATA_COLLECTOR: str = None
