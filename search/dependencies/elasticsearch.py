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

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from search.config import Settings
from search.config import get_settings


async def get_elasticsearch_client(settings: Settings = Depends(get_settings)) -> AsyncElasticsearch:
    """Create a FastAPI callable dependency for async Elasticsearch client instance."""

    client = AsyncElasticsearch(settings.ELASTICSEARCH_URI)

    try:
        yield client
    finally:
        await client.close()
