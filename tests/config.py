import os
from pydantic import BaseSettings


class Config(BaseSettings):
    INSTANCE: str
    USER_AGENT: str = None
    HEADLESS: bool = True
    BROWSER: list = None
    WINDOW_HEIGHT: int = 1400
    WINDOW_WIDTH: int = 1400
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

    class Config:
        env_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))), ".env"
        )
