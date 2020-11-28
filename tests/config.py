from functools import lru_cache
import os
from pydantic import BaseSettings


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class Config(BaseSettings):
    INSTANCE: str = "development"
    HEADLESS: bool = True
    WINDOW_HEIGHT: int = 1440
    WINDOW_WIDTH: int = 1440
    BROWSERS: list = ["firefox", "chrome"]
    INSTANCE_DATA_DIR: str = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "data/instances",
        os.getenv("INSTANCE"),
    )
    TEST_USER_NORMAL: str = None
    TEST_USER_NORMAL_NAME: str = None
    TEST_USER_NORMAL_PWD: str = None


class ProductionConfig(Config):
    class Config:
        env_file = os.path.join(ROOT_DIR, ".env.dataverse_production")


class LocalhostT550Config(Config):
    class Config:
        env_file = os.path.join(ROOT_DIR, ".env.dataverse_localhost_t550")


class DV03Config(Config):
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
