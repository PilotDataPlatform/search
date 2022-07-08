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

from search.components import ItemActivity
from search.components import ModelList
from search.components.item_activity.crud import ItemActivityCRUD
from search.components.item_activity.models import ItemActivityType
from search.components.item_activity.schemas import ItemActivitySchema
from search.components.models import ContainerType
from tests.fixtures.components._base_factory import BaseFactory


class ItemActivityFactory(BaseFactory):
    """Create item activity related entries for testing purposes."""

    def generate(
        self,
        id_: str = ...,
        activity_type: ItemActivityType = ...,
        activity_time: datetime = ...,
        container_code: str = ...,
        container_type: ContainerType = ...,
    ) -> ItemActivitySchema:
        if id_ is ...:
            id_ = self.fake.uuid4()

        if activity_type is ...:
            activity_type = random.choice(ItemActivityType.values())

        if activity_time is ...:
            activity_time = self.fake.past_datetime()

        if container_code is ...:
            container_code = self.fake.word().lower()

        if container_type is ...:
            container_type = ContainerType.PROJECT

        return ItemActivitySchema(
            id=id_,
            activity_type=activity_type,
            activity_time=activity_time,
            container_code=container_code,
            container_type=container_type,
        )

    async def create(
        self,
        id_: str = ...,
        activity_type: ItemActivityType = ...,
        activity_time: datetime = ...,
        container_code: str = ...,
        container_type: ContainerType = ...,
        **kwds: Any,
    ) -> ItemActivity:
        entry = self.generate(id_, activity_type, activity_time, container_code, container_type)

        # Make the document immediately appear in search results
        # https://www.elastic.co/guide/en/elasticsearch/reference/7.17/docs-refresh.html#docs-refresh
        params = {'refresh': 'true'}

        return await self.crud.create(entry, params=params, **kwds)

    async def bulk_create(
        self,
        number: int,
        id_: str = ...,
        activity_type: ItemActivityType = ...,
        activity_time: datetime = ...,
        container_code: str = ...,
        container_type: ContainerType = ...,
        **kwds: Any,
    ) -> ModelList[ItemActivity]:
        return ModelList(
            [
                await self.create(id_, activity_type, activity_time, container_code, container_type, **kwds)
                for _ in range(number)
            ]
        )


@pytest.fixture
def item_activity_crud(es_client) -> ItemActivityCRUD:
    yield ItemActivityCRUD(es_client)


@pytest.fixture
async def item_activity_factory(item_activity_crud, fake) -> ItemActivityFactory:
    item_activity_factory = ItemActivityFactory(item_activity_crud, fake)

    await item_activity_factory.create_index()
    yield item_activity_factory
    await item_activity_factory.delete_index()
