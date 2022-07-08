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

from search.components.crud import CRUD
from search.components.item_activity.models import ItemActivity
from search.components.item_activity.models import ItemActivityTransferStatistics
from search.components.item_activity.models import ItemActivityType
from search.components.models import ContainerType
from search.components.search_query import SearchQuery


class ItemActivityCRUD(CRUD):
    """CRUD for managing documents in items-activity-logs index."""

    index = 'items-activity-logs'
    model = ItemActivity

    async def get_project_transfer_statistics(
        self, project_code: str, date: datetime, time_zone: str
    ) -> ItemActivityTransferStatistics:
        """Get aggregated project transfer statistics."""

        parsed_tz = datetime.strptime(time_zone, '%z')
        day_with_timezone = date.astimezone(tz=parsed_tz.tzinfo)
        day = day_with_timezone.date().isoformat()

        search_query = SearchQuery()
        search_query.match_term('container_type', ContainerType.PROJECT.value)
        search_query.match_term('container_code', project_code)
        search_query.match_range('activity_time', gte=day, lte=day)
        search_query.match_multiple_terms(
            'activity_type', [ItemActivityType.UPLOAD.value, ItemActivityType.DOWNLOAD.value]
        )
        query = search_query.build()

        aggregations = {'activity_types': {'terms': {'field': 'activity_type.keyword'}}}

        result = await self._search(query=query, size=0, aggregations=aggregations)

        mapping = {
            ItemActivityType.UPLOAD: 0,
            ItemActivityType.DOWNLOAD: 0,
        }

        for bucket in result['aggregations']['activity_types']['buckets']:
            try:
                mapping[bucket['key']] += 1
            except KeyError:
                pass

        return ItemActivityTransferStatistics(
            uploaded=mapping[ItemActivityType.UPLOAD],
            downloaded=mapping[ItemActivityType.DOWNLOAD],
        )
