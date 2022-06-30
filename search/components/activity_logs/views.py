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
from typing import Optional

from common import LoggerFactory
from fastapi import APIRouter

from search.components.es_helper import search
from search.schemas.base import APIResponse
from search.schemas.base import EAPIResponseCode

_API_NAMESPACE = 'api_activity_logs'

__logger = LoggerFactory(_API_NAMESPACE).get_logger()

router = APIRouter(prefix='/activity-logs', tags=['Activity Logs Query'])


@router.get('', summary='list activity logs.')
async def query_activity_logs(
    query: str,
    page: Optional[int] = 0,
    page_size: Optional[int] = 10,
    sort_by: Optional[str] = 'create_timestamp',
    sort_type: Optional[str] = 'desc',
) -> APIResponse:
    response = APIResponse()
    queries = json.loads(query)
    search_params = []

    __logger.info(f'activity logs query: {query}')

    try:
        for key in queries:
            if key == 'create_timestamp':
                filed_params = {
                    'nested': False,
                    'field': key,
                    'range': queries[key]['value'],
                    'multi_values': False,
                    'search_type': queries[key]['condition'],
                }
                search_params.append(filed_params)
            else:
                filed_params = {
                    'nested': False,
                    'field': key,
                    'range': False,
                    'multi_values': False,
                    'value': queries[key]['value'],
                    'search_type': queries[key]['condition'],
                }
                search_params.append(filed_params)

        res = await search('activity-logs', page, page_size, search_params, sort_by, sort_type)

        __logger.info(f'activity logs result: {res}')

        response.code = EAPIResponseCode.success
        response.result = res['hits']['hits']
        response.total = res['hits']['total']['value']
        return response
    except Exception as e:
        __logger.error(f'activity logs error: {str(e)}')
        response.code = EAPIResponseCode.internal_error
        response.result = {'errors': str(e)}
        return response
