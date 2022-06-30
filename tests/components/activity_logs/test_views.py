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

import json

import pytest

pytestmark = pytest.mark.asyncio


async def test_activity_logs_should_get_data_from_elasticsearch(client, httpx_mock):
    query = json.dumps(
        {'dataset_geid': {'value': '679e4b11-61fd-4df7-9084-5e0ff0c99b9e-1647523203', 'condition': 'equal'}}
    )
    query_string = f'page_size=10&page=0&order_by=create_timestamp&order_type=desc&query={query}'

    httpx_mock.add_response(
        method='GET',
        url='http://elastic_search_service/activity-logs/_search',
        json={'hits': {'hits': {'any': 'any'}, 'total': {'value': 1}}},
    )

    res = await client.get(f'/v1/activity-logs?{query_string}')

    assert res.status_code == 200
    assert res.json()['result'] == {'any': 'any'}
    assert res.json()['total'] == 1
