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

from typing import Any

from search.components.crud import CRUD
from search.components.metadata_item.crud.size_usage import SizeUsageHandler
from search.components.metadata_item.filtering import MetadataItemProjectSizeUsageFiltering
from search.components.metadata_item.models import MetadataItem
from search.components.metadata_item.models import MetadataItemSizeStatistics
from search.components.metadata_item.models import MetadataItemSizeUsage
from search.components.metadata_item.models import MetadataItemType
from search.components.metadata_item.models import SizeGroupBy
from search.components.metadata_item.pagination import MetadataItemPage
from search.components.models import ContainerType
from search.components.pagination import Pagination
from search.components.search_query import SearchQuery


class MetadataItemCRUD(CRUD):
    """CRUD for managing documents in metadata-items index."""

    index = 'metadata-items'
    model = MetadataItem

    def _get_group_by_zone_aggregation(self) -> dict[str, Any]:
        """Get aggregation for grouping by zone."""

        return {'terms': {'field': 'zone'}}

    def _process_group_by_zone_aggregation(self, aggregation: dict[str, Any]) -> dict[int, int]:
        """Process grouping by zone aggregation results."""

        return {bucket['key']: bucket['doc_count'] for bucket in aggregation['buckets']}

    async def _list(self, **kwds: Any) -> dict[str, Any]:
        """Get a list of entries by executing a search.

        Add extra total_per_zone aggregation that applies same query per each zone.
        """

        aggregations = {'total_per_zone': self._get_group_by_zone_aggregation()}

        return await self._search(aggregations=aggregations, **kwds)

    async def _paginate_list_result(self, result: dict[str, Any], pagination: Pagination) -> MetadataItemPage:
        """Create a response page from list result.

        Add extra total_per_zone attribute based on aggregated count per each zone.
        """

        count = result['hits']['total']['value']
        entries = self._parse_documents(result['hits']['hits'])
        total_per_zone = self._process_group_by_zone_aggregation(result['aggregations']['total_per_zone'])

        return MetadataItemPage(pagination=pagination, count=count, entries=entries, total_per_zone=total_per_zone)

    async def get_project_size_usage(
        self, filtering: MetadataItemProjectSizeUsageFiltering, time_zone: str, group_by: SizeGroupBy
    ) -> MetadataItemSizeUsage:
        """Get aggregated project storage usage filtered by dates and grouped into separate buckets."""

        search_query = SearchQuery()
        filtering.apply(search_query)
        query = search_query.build()

        size_usage_handler = SizeUsageHandler(
            from_date=filtering.from_date, to_date=filtering.to_date, time_zone=time_zone, group_by=group_by
        )
        aggregations = size_usage_handler.get_aggregations()

        result = await self._search(query=query, size=0, aggregations=aggregations)

        return size_usage_handler.process_search_result(result)

    async def get_project_statistics(self, project_code: str) -> MetadataItemSizeStatistics:
        """Get aggregated project files statistics."""

        search_query = SearchQuery()
        search_query.match_term('type', MetadataItemType.FILE.value)
        search_query.match_term('container_type', ContainerType.PROJECT.value)
        search_query.match_term('container_code', project_code)
        query = search_query.build()

        aggregations = {
            'size': {'sum': {'field': 'size'}},
            'zone': self._get_group_by_zone_aggregation(),
        }

        result = await self._search(query=query, size=0, aggregations=aggregations)

        count = result['hits']['total']['value']
        size = int(result['aggregations']['size']['value'])
        count_by_zone = self._process_group_by_zone_aggregation(result['aggregations']['zone'])

        return MetadataItemSizeStatistics(count=count, size=size, count_by_zone=count_by_zone)
