import os
import sys
from typing import List

from pydantic import BaseSettings

if os.getenv("ENV_FILE"):
    ENV_FILE_BASE = str(os.path.splitext(os.path.basename(os.getenv("ENV_FILE")))[0])
else:
    sys.exit("ERROR: 'ENV_FILE' missing.")


class UtilsSettings(BaseSettings):
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
