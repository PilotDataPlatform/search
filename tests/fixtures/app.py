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
from contextlib import AbstractContextManager
from typing import Any
from typing import Callable

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from search.app import create_app
from search.config import Settings
from search.config import get_settings


class OverrideDependencies(AbstractContextManager):
    """Temporarily override application dependencies using context manager."""

    def __init__(self, app: FastAPI) -> None:
        self.app = app
        self.stashed_dependencies = {}
        self.dependencies_to_override = {}

    def __call__(self, dependencies: dict[Callable[..., Any], Callable[..., Any]]) -> 'OverrideDependencies':
        self.dependencies_to_override = dependencies
        return self

    def __enter__(self) -> 'OverrideDependencies':
        self.stashed_dependencies = self.app.dependency_overrides.copy()
        self.app.dependency_overrides.update(self.dependencies_to_override)
        return self

    def __exit__(self, *args: Any) -> None:
        self.app.dependency_overrides.clear()
        self.app.dependency_overrides.update(self.stashed_dependencies)
        self.dependencies_to_override = {}
        return None


@pytest.fixture
def override_dependencies(app) -> OverrideDependencies:
    yield OverrideDependencies(app)


@pytest.fixture(scope='session')
def event_loop() -> AbstractEventLoop:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def settings() -> Settings:
    settings = Settings()
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
