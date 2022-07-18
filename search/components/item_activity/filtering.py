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
from search.components.item_activity.models import ItemActivityType
from search.components.models import ContainerType
from search.components.search_query import SearchQuery


class ItemActivityProjectFileActivityFiltering(Filtering):
    """Item activities filtering for project file activity."""

    project_code: str
    activity_type: ItemActivityType
    from_date: datetime
    to_date: datetime

    def apply(self, search_query: SearchQuery) -> None:
        """Add filtering into search query."""

        search_query.match_term('container_type', ContainerType.PROJECT.value)
        search_query.match_term('container_code', self.project_code)
        search_query.match_term('activity_type', self.activity_type.value)
        search_query.match_range('activity_time', gte=self.from_date.isoformat(), lt=self.to_date.isoformat())
