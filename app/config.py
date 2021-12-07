from pydantic import BaseSettings, Extra
from functools import lru_cache

class Settings(BaseSettings):
    port: int = 5080
    host: str = "0.0.0.0"
    log_level: str = "info"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.allow

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                env_settings,
                init_settings,
                file_secret_settings,
            )

@lru_cache(1)
def get_settings() -> Settings:
    settings =  Settings()
    return settings
