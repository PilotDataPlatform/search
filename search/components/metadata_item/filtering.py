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

from search.components.filtering import Filtering
from search.components.models import ContainerType
from search.components.search_query import SearchQuery


class MetadataItemFiltering(Filtering):
    """Metadata items filtering control parameters."""

    name: str | None = None
    owner: str | None = None
    zone: int | None = None
    container_code: str | None = None
    container_type: ContainerType | None = None
    created_time_start: datetime | None = None
    created_time_end: datetime | None = None
    size_gte: int | None = None
    size_lte: int | None = None
    is_archived: bool | None = None

    def apply(self, search_query: SearchQuery) -> None:  # noqa: C901
        """Add filtering into search query."""

        if self.name:
            search_query.match_keyword('name', self.name)

        if self.owner:
            search_query.match_keyword('owner', self.owner)

        if self.zone is not None:
            search_query.match_term('zone', self.zone)

        if self.container_code:
            search_query.match_term('container_code', self.container_code)

        if self.container_type:
            search_query.match_term('container_type', self.container_type.value)

        if self.created_time_start:
            search_query.match_range('created_time', gte=self.created_time_start.isoformat())

        if self.created_time_end:
            search_query.match_range('created_time', lte=self.created_time_end.isoformat())

        if self.size_gte:
            search_query.match_range('size', gte=self.size_gte)

        if self.size_lte:
            search_query.match_range('size', lte=self.size_lte)

        if self.is_archived is not None:
            search_query.match_term('archived', self.is_archived)


class MetadataItemProjectSizeUsageFiltering(Filtering):
    """Metadata items filtering for project size usage."""

    project_code: str
    from_date: datetime
    to_date: datetime

    def apply(self, search_query: SearchQuery) -> None:
        """Add filtering into search query."""

        search_query.match_term('container_type', ContainerType.PROJECT.value)
        search_query.match_term('container_code', self.project_code)
        search_query.match_range('created_time', gte=self.from_date.isoformat(), lt=self.to_date.isoformat())
