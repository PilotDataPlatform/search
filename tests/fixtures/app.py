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

import asyncio
from asyncio import AbstractEventLoop
from pathlib import Path
from typing import Callable

import pytest
import yaml
from fastapi import FastAPI
from httpx import AsyncClient

from search.app import create_app
from search.config import Settings
from search.config import get_settings


@pytest.fixture(scope='session')
def project_root() -> Path:
    path = Path(__file__)

    while path.name != 'search':
        path = path.parent

    yield path


@pytest.fixture(scope='session')
def get_service_image(project_root) -> Callable[[str], str]:
    with open(project_root / 'docker-compose.yaml') as file:
        services = yaml.safe_load(file)['services']

    def get_image(service_name: str) -> str:
        return services[service_name]['image']

    yield get_image


@pytest.fixture(scope='session')
def event_loop() -> AbstractEventLoop:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    yield loop
    loop.close()


@pytest.fixture(scope='session')
def settings(elasticsearch_uri) -> Settings:
    settings = Settings(ELASTICSEARCH_URI=elasticsearch_uri)
    yield settings


@pytest.fixture
def app(event_loop, settings) -> FastAPI:
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: settings
    yield app


@pytest.fixture
async def client(app) -> AsyncClient:
    async with AsyncClient(app=app, base_url='https://') as client:
        yield client
