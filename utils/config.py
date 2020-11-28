from functools import lru_cache
import os
from pydantic import BaseSettings


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class Config(BaseSettings):
    INSTANCE: str = "development"
    BASE_URL: str = None
    API_TOKEN: str = None
    UTILS_DATA_DIR: str = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "data/instances",
        os.getenv("INSTANCE"),
    )
    FILENAME_TREE: str = "tree.json"
    FILENAME_DATAVERSES: str = "dataverses.json"
    FILENAME_DATASETS: str = "datasets.json"
    FILENAME_DATAFILES: str = "datafiles.json"
    FILENAME_METADATA: str = "metadata.json"
    ROOT_DIR: str = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class ProductionConfig(Config):
    INSTANCE_TYPE: str = "production"

    class Config:
        env_file = os.path.join(ROOT_DIR, ".env.dataverse_production")


class LocalhostT550Config(Config):
    INSTANCE_TYPE: str = "development"

    class Config:
        env_file = os.path.join(ROOT_DIR, ".env.dataverse_localhost_t550")


class DV03Config(Config):
    INSTANCE_TYPE: str = "testing"

    class Config:
        env_file = os.path.join(ROOT_DIR, ".env.dataverse_dv03")


def get_config_name():
    return os.getenv("INSTANCE") or "development"


def get_config(config_name="default"):
    configs = {
        "dataverse_production": ProductionConfig(),
        "dataverse_localhost_t550": LocalhostT550Config(),
        "dataverse_dv03": DV03Config(),
        "default": LocalhostT550Config(),
    }
    return configs[config_name]
