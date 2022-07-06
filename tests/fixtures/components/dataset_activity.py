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

import random
from datetime import datetime
from typing import Any

import pytest

from search.components import DatasetActivity
from search.components import ModelList
from search.components.dataset_activity.crud import DatasetActivityCRUD
from search.components.dataset_activity.schemas import DatasetActivitySchema
from tests.fixtures.components._base_factory import BaseFactory


class DatasetActivityFactory(BaseFactory):
    """Create dataset activity related entries for testing purposes."""

    def generate(
        self,
        activity_type: str = ...,
        activity_time: datetime = ...,
        container_code: str = ...,
        version: str = ...,
        target_name: str = ...,
        user: str = ...,
        changes: list[dict[str, Any]] = ...,
    ) -> DatasetActivitySchema:

        if activity_type is ...:
            activity_type = random.choice(['create', 'update', 'schema_update', 'publish'])

        if activity_time is ...:
            activity_time = self.fake.past_datetime()

        if container_code is ...:
            container_code = self.fake.unique.word().lower()

        if version is ...:
            version = f'{self.fake.pyint(0, 4)}.{self.fake.pyint(0, 20)}'

        if target_name is ...:
            target_name = '.'.join(self.fake.words(3)).lower()

        if user is ...:
            user = f'{self.fake.pystr()}-{self.fake.first_name()}'.lower()

        if changes is ...:
            changes = []

        return DatasetActivitySchema(
            activity_type=activity_type,
            activity_time=activity_time,
            container_code=container_code,
            version=version,
            target_name=target_name,
            user=user,
            changes=changes,
        )

    async def create(
        self,
        activity_type: str = ...,
        activity_time: datetime = ...,
        container_code: str = ...,
        version: str = ...,
        target_name: str = ...,
        user: str = ...,
        changes: list[dict[str, Any]] = ...,
        **kwds: Any,
    ) -> DatasetActivity:
        entry = self.generate(
            activity_type,
            activity_time,
            container_code,
            version,
            target_name,
            user,
            changes,
        )

        # Make the document immediately appear in search results
        # https://www.elastic.co/guide/en/elasticsearch/reference/7.17/docs-refresh.html#docs-refresh
        params = {'refresh': 'true'}

        return await self.crud.create(entry, params=params, **kwds)

    async def bulk_create(
        self,
        number: int,
        activity_type: str = ...,
        activity_time: datetime = ...,
        container_code: str = ...,
        version: str = ...,
        target_name: str = ...,
        user: str = ...,
        changes: list[dict[str, Any]] = ...,
        **kwds: Any,
    ) -> ModelList[DatasetActivity]:
        return ModelList(
            [
                await self.create(
                    activity_type,
                    activity_time,
                    container_code,
                    version,
                    target_name,
                    user,
                    changes,
                    **kwds,
                )
                for _ in range(number)
            ]
        )


@pytest.fixture
def dataset_activity_crud(es_client) -> DatasetActivityCRUD:
    yield DatasetActivityCRUD(es_client)


@pytest.fixture
async def dataset_activity_factory(dataset_activity_crud, fake) -> DatasetActivityFactory:
    dataset_activity_factory = DatasetActivityFactory(dataset_activity_crud, fake)

    await dataset_activity_factory.create_index()
    yield dataset_activity_factory
    await dataset_activity_factory.delete_index()
