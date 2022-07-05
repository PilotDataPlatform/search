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

from datetime import datetime

from fastapi import Query
from pydantic import PositiveInt

from search.components.metadata_item.filtering import MetadataItemFiltering
from search.components.parameters import FilterParameters
from search.components.parameters import SortByFields


class MetadataItemSortByFields(SortByFields):
    """Fields by which metadata items can be sorted."""

    SIZE = 'size'
    CREATED_TIME = 'created_time'
    LAST_UPDATED_TIME = 'last_updated_time'


class MetadataItemFilterParameters(FilterParameters):
    """Query parameters for metadata items filtering."""

    name: str | None = Query(default=None)
    owner: str | None = Query(default=None)
    zone: int | None = Query(default=None)
    container_code: str | None = Query(default=None)
    container_type: str | None = Query(default=None)
    created_time_start: datetime | None = Query(default=None)
    created_time_end: datetime | None = Query(default=None)
    size_gte: PositiveInt | None = Query(default=None)
    size_lte: PositiveInt | None = Query(default=None)
    is_archived: bool | None = Query(default=None)

    def to_filtering(self) -> MetadataItemFiltering:
        return MetadataItemFiltering(
            name=self.name,
            owner=self.owner,
            zone=self.zone,
            container_code=self.container_code,
            container_type=self.container_type,
            created_time_start=self.created_time_start,
            created_time_end=self.created_time_end,
            size_gte=self.size_gte,
            size_lte=self.size_lte,
            is_archived=self.is_archived,
        )
