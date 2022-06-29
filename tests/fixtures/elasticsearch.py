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

import pytest
from elasticsearch import AsyncElasticsearch
from testcontainers.elasticsearch import ElasticSearchContainer


@pytest.fixture(scope='session')
def elasticsearch_uri(get_service_image) -> str:
    elasticsearch_image = get_service_image('elasticsearch')

    with ElasticSearchContainer(elasticsearch_image) as es_container:
        yield es_container.get_url()


@pytest.fixture(scope='session')
async def es_client(settings) -> AsyncElasticsearch:
    client = AsyncElasticsearch(settings.ELASTICSEARCH_URI)

    try:
        yield client
    finally:
        await client.close()
