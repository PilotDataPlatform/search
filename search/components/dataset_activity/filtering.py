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
from search.components.search_query import SearchQuery


class DatasetActivityFiltering(Filtering):
    """Dataset activity filtering control parameters."""

    activity_type: str | None = None
    activity_time_start: datetime | None = None
    activity_time_end: datetime | None = None
    container_code: str | None = None
    version: str | None = None
    target_name: str | None = None
    user: str | None = None

    def apply(self, search_query: SearchQuery) -> None:  # noqa: C901
        """Add filtering into search query."""

        if self.activity_type:
            search_query.match_term('activity_type', self.activity_type)

        if self.activity_time_start:
            search_query.match_range('activity_time', gte=self.activity_time_start.isoformat())

        if self.activity_time_end:
            search_query.match_range('activity_time', lte=self.activity_time_end.isoformat())

        if self.container_code:
            search_query.match_term('container_code', self.container_code)

        if self.version:
            search_query.match_keyword('version', self.version)

        if self.target_name:
            search_query.match_keyword('target_name', self.target_name)

        if self.user:
            search_query.match_keyword('user', self.user)
