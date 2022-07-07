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

from search.components import MetadataItem
from search.components import ModelList
from search.components.metadata_item.crud import MetadataItemCRUD
from search.components.metadata_item.schemas import MetadataItemSchema
from tests.fixtures.components._base_factory import BaseFactory


class MetadataItemFactory(BaseFactory):
    """Create metadata item related entries for testing purposes."""

    def generate(  # noqa: C901
        self,
        id_: str = ...,
        parent_path: str | None = ...,
        type_: str = ...,
        zone: int = ...,
        name: str = ...,
        size: int = ...,
        owner: str = ...,
        container_code: str = ...,
        container_type: str = ...,
        created_time: datetime = ...,
        last_updated_time: datetime = ...,
        tags: list[str] = ...,
        template_name: str = ...,
        attributes: list[dict[str, Any]] = ...,
        archived: bool = ...,
    ) -> MetadataItemSchema:
        unique_prefix = self.fake.pystr()

        if id_ is ...:
            id_ = self.fake.uuid4()

        if parent_path is ...:
            parent_path = '.'.join(self.fake.words(4)).lower()

        if type_ is ...:
            type_ = random.choice(['file', 'folder'])

        if zone is ...:
            zone = self.fake.pyint(0, 1)

        if name is ...:
            name = f'{unique_prefix}-{self.fake.file_name()}'.lower()

        if size is ...:
            size = self.fake.pyint()

        if owner is ...:
            owner = f'{unique_prefix}-{self.fake.first_name()}'.lower()

        if container_code is ...:
            container_code = self.fake.word().lower()

        if container_type is ...:
            container_type = 'project'

        if created_time is ...:
            created_time = self.fake.past_datetime()

        if last_updated_time is ...:
            last_updated_time = self.fake.past_datetime()

        if tags is ...:
            tags = self.fake.words(3, unique=True)

        if template_name is ...:
            template_name = self.fake.word().lower()

        if attributes is ...:
            attributes = []

        if archived is ...:
            archived = False

        return MetadataItemSchema(
            id=id_,
            parent_path=parent_path,
            type=type_,
            zone=zone,
            name=name,
            size=size,
            owner=owner,
            container_code=container_code,
            container_type=container_type,
            created_time=created_time,
            last_updated_time=last_updated_time,
            tags=tags,
            template_name=template_name,
            attributes=attributes,
            archived=archived,
        )

    async def create(
        self,
        id_: str = ...,
        parent_path: str | None = ...,
        type_: str = ...,
        zone: int = ...,
        name: str = ...,
        size: int = ...,
        owner: str = ...,
        container_code: str = ...,
        container_type: str = ...,
        created_time: datetime = ...,
        last_updated_time: datetime = ...,
        tags: list[str] = ...,
        template_name: str = ...,
        attributes: list[dict[str, Any]] = ...,
        archived: bool = ...,
        **kwds: Any,
    ) -> MetadataItem:
        entry = self.generate(
            id_,
            parent_path,
            type_,
            zone,
            name,
            size,
            owner,
            container_code,
            container_type,
            created_time,
            last_updated_time,
            tags,
            template_name,
            attributes,
            archived,
        )

        # Make the document immediately appear in search results
        # https://www.elastic.co/guide/en/elasticsearch/reference/7.17/docs-refresh.html#docs-refresh
        params = {'refresh': 'true'}

        return await self.crud.create(entry, params=params, **kwds)

    async def bulk_create(
        self,
        number: int,
        id_: str = ...,
        parent_path: str | None = ...,
        type_: str = ...,
        zone: int = ...,
        name: str = ...,
        size: int = ...,
        owner: str = ...,
        container_code: str = ...,
        container_type: str = ...,
        created_time: datetime = ...,
        last_updated_time: datetime = ...,
        tags: list[str] = ...,
        template_name: str = ...,
        attributes: list[dict[str, Any]] = ...,
        archived: bool = ...,
        **kwds: Any,
    ) -> ModelList[MetadataItem]:
        return ModelList(
            [
                await self.create(
                    id_,
                    parent_path,
                    type_,
                    zone,
                    name,
                    size,
                    owner,
                    container_code,
                    container_type,
                    created_time,
                    last_updated_time,
                    tags,
                    template_name,
                    attributes,
                    archived,
                    **kwds,
                )
                for _ in range(number)
            ]
        )


@pytest.fixture
def metadata_item_crud(es_client) -> MetadataItemCRUD:
    yield MetadataItemCRUD(es_client)


@pytest.fixture
async def metadata_item_factory(metadata_item_crud, fake) -> MetadataItemFactory:
    metadata_item_factory = MetadataItemFactory(metadata_item_crud, fake)

    await metadata_item_factory.create_index()
    yield metadata_item_factory
    await metadata_item_factory.delete_index()
