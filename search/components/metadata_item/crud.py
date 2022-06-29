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
from search.components.metadata_item.models import MetadataItem
from search.components.metadata_item.pagination import MetadataItemPage
from search.components.pagination import Pagination


class MetadataItemCRUD(CRUD):
    """CRUD for managing documents in metadata-items index."""

    index = 'metadata-items'
    model = MetadataItem

    async def _list(self, **kwds: Any) -> dict[str, Any]:
        """Get a list of entries by executing a search.

        Add extra total_per_zone aggregation that applies same query per by zone.
        """

        aggregations = {'total_per_zone': {'terms': {'field': 'zone'}}}

        return await self._search(aggregations=aggregations, **kwds)

    async def _paginate_list_result(self, result: dict[str, Any], pagination: Pagination) -> MetadataItemPage:
        """Create a response page from list result.

        Add extra total_per_zone attribute based on aggregated count per each zone.
        """

        count = result['hits']['total']['value']
        entries = self._parse_documents(result['hits']['hits'])
        total_per_zone = {
            bucket['key']: bucket['doc_count'] for bucket in result['aggregations']['total_per_zone']['buckets']
        }

        return MetadataItemPage(pagination=pagination, count=count, entries=entries, total_per_zone=total_per_zone)
