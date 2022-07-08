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

from __future__ import annotations

from datetime import datetime

from search.components.models import ContainerType
from search.components.pagination import PageType
from search.components.schemas import BaseSchema
from search.components.schemas import ListResponseSchema


class MetadataItemAttributeSchema(BaseSchema):
    """General metadata item attribute schema."""

    name: str


class MetadataItemSchema(BaseSchema):
    """General metadata item schema."""

    id: str
    parent_path: str | None
    type: str
    zone: int
    name: str
    size: int
    owner: str
    container_code: str
    container_type: ContainerType
    created_time: datetime
    last_updated_time: datetime
    tags: list[str]
    template_name: str
    attributes: list[MetadataItemAttributeSchema]
    archived: bool


class MetadataItemResponseSchema(MetadataItemSchema):
    """Default schema for single metadata item in response."""

    pk: str


class MetadataItemListResponseSchema(ListResponseSchema):
    """Default schema for multiple metadata items in response."""

    total_per_zone: dict[int, int]
    result: list[MetadataItemResponseSchema]

    @classmethod
    def from_page(cls, page: PageType) -> MetadataItemListResponseSchema:
        return cls(
            num_of_pages=page.total_pages,
            page=page.number,
            total=page.count,
            total_per_zone=page.total_per_zone,
            result=page.entries,
        )
