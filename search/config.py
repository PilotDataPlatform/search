# Copyright (C) 2022 Indoc Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from functools import lru_cache

from pydantic import BaseSettings
from pydantic import Extra


class Settings(BaseSettings):
    """Store service configuration settings."""

    APP_NAME: str = 'search'
    VERSION: str = '0.1.0'
    ENV: str = ''
    HOST: str = '127.0.0.1'
    PORT: int = 5064
    WORKERS: int = 1

    OPEN_TELEMETRY_ENABLED: bool = False
    OPEN_TELEMETRY_HOST: str = '127.0.0.1'
    OPEN_TELEMETRY_PORT: int = 6831

    ELASTIC_SEARCH_SERVICE: str = ''

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.ignore


@lru_cache(1)
def get_settings() -> Settings:
    settings = Settings()
    return settings
