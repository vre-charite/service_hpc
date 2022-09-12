# Copyright 2022 Indoc Research
# 
# Licensed under the EUPL, Version 1.2 or – as soon they
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
# 
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
# 

import os
from pydantic import BaseSettings, Extra
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()
SRV_NAMESPACE = os.environ.get("APP_NAME", "service_hpc")

class Settings(BaseSettings):
    port: int = 5080
    host: str = "0.0.0.0"
    log_level: str = "info"
    OPEN_TELEMETRY_ENABLED: str = "FALSE"

    def modify_values(self, settings):
        settings.opentelemetry_enabled = settings.OPEN_TELEMETRY_ENABLED == "TRUE"
        return settings

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
def get_settings():
    settings = Settings()
    settings.modify_values(settings)
    return settings


ConfigClass = get_settings()
