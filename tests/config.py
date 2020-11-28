from functools import lru_cache
import os
from pydantic import BaseSettings


class Config(BaseSettings):
    INSTANCE: str = None
    HEADLESS: bool = True
    WINDOW_HEIGHT: int = 1440
    WINDOW_WIDTH: int = 1440
    BROWSERS: list = ["firefox", "chrome"]
    DATA_DIR: str = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "data/instances",
        os.getenv("INSTANCE"),
    )
    API_TOKEN: str = None
    TEST_USER_NORMAL: str = None
    TEST_USER_NORMAL_NAME: str = None
    TEST_USER_NORMAL_PWD: str = None


class DevelopmentConfig(Config):
    pass


class JenkinsConfig(Config):
    pass


def get_config_name():
    return os.getenv("TEST_CONFIG") or "default"


def get_config(config_name="default"):
    configs = {
        "development": DevelopmentConfig(),
        "jenkins": JenkinsConfig(),
        "default": JenkinsConfig(),
    }
    return configs[config_name]
