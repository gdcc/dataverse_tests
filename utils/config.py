import os
from pydantic import BaseSettings


class Config(BaseSettings):
    INSTANCE: str
    BASE_URL: str = None
    API_TOKEN: str = None
    PRODUCTION: bool = False
    FILENAME_TREE: str = "tree.json"
    FILENAME_DATAVERSES: str = "dataverses.json"
    FILENAME_DATASETS: str = "datasets.json"
    FILENAME_DATAFILES: str = "datafiles.json"
    FILENAME_METADATA: str = "metadata.json"

    class Config:
        env_file = ".env"
