from pydantic import BaseSettings


class UtilsConfig(BaseSettings):
    INSTANCE: str
    BASE_URL: str = None
    API_TOKEN: str = None
    PRODUCTION: bool = False
    FILENAME_DATAVERSES: str = "dataverses.json"
    FILENAME_DATASETS: str = "datasets.json"
    FILENAME_DATAFILES: str = "datafiles.json"
    FILENAME_METADATA: str = "metadata.json"
    USER_NORMAL_PWD: str = None
    BUILTIN_USER_KEY: str = None


class TestingConfig(BaseSettings):
    INSTANCE: str
    USER_FILENAME: str
    BASE_URL: str = None
    API_TOKEN: str = ""
    USER_AGENT: str = None
    HEADLESS: bool = True
    BROWSER: list = None
    WINDOW_HEIGHT: int = 1400
    WINDOW_WIDTH: int = 1400
    USER_SUPERUSER: str = None
    USER_SUPERUSER_PWD: str = None
    USER_NORMAL: str = None
    USER_NORMAL_NAME: str = None
    USER_NORMAL_PWD: str = None
    USER_SHIBBOLETH: str = None
    USER_SHIBBOLETH_NAME: str = None
    USER_SHIBBOLETH_PWD: str = None
    TEST_CONFIG_FILENAME: str = "test-config.json"
    FILENAME_DATAVERSES: str = "dataverses.json"
    FILENAME_DATASETS: str = "datasets.json"
    FILENAME_DATAFILES: str = "datafiles.json"
    FILENAME_METADATA: str = "metadata.json"
    USER_NORMAL_PWD: str = None
    BUILTIN_USER_KEY: str = None
