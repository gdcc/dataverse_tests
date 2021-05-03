from typing import List

from pydantic import BaseSettings


class UtilsSettings(BaseSettings):
    BASE_URL: str
    INSTANCE: str
    PRODUCTION: bool = False
    FILENAME_DATAVERSES: str = "dataverses.json"
    FILENAME_DATASETS: str = "datasets.json"
    FILENAME_DATAFILES: str = "datafiles.json"
    FILENAME_METADATA: str = "metadata.json"
    BUILTIN_USER_KEY: str = None


class TestSettings(BaseSettings):
    BASE_URL: str
    INSTANCE: str
    USER_FILENAME: str
    DATA_COLLECTOR: str
    HEADLESS: bool = True
    USER_AGENT: str = "TESTING"
    WINDOW_HEIGHT: int = 1400
    WINDOW_WIDTH: int = 1600
    MAX_WAIT_TIME: int = 10
    LOGIN_OPTIONS: List[str] = ["normal"]
    FILENAME_DATAVERSES: str = "dataverses.json"
    FILENAME_DATASETS: str = "datasets.json"
    FILENAME_DATAFILES: str = "datafiles.json"
    FILENAME_METADATA: str = "metadata.json"
    SHIBBOLETH_INSTITUTION: str = None
    SHIBBOLETH_LOGIN_PAGE_TITLE: str = None
    BUILTIN_USER_KEY: str = None
