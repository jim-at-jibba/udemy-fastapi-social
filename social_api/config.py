from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False


class DevConfig(GlobalConfig):
    # dev configuration will be prefixed with DEV_
    # pydantic will strip out the DEV_ prefix and just use the variable name
    model_config = SettingsConfigDict(env_prefix="DEV_")


class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_")


class TestConfig(GlobalConfig):
    DATABASE_URL: Optional[str] = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = True
    model_config = SettingsConfigDict(env_prefix="TEST_")


@lru_cache()
def get_config(env_state: str | None):
    # This should only be run once and so should not change
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    if env_state is not None:
        print(f"env_state: {env_state}, {configs[env_state]}")
        return configs[env_state]()
    else:
        raise ValueError(f"Invalid env_state value: {env_state}")


config = get_config(BaseConfig().ENV_STATE)
