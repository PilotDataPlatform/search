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

from common import LoggerFactory
from httpx import AsyncClient

from search.config import get_settings

__logger = LoggerFactory('es_helper').get_logger()

config = get_settings()


def _nested(item: dict) -> dict:
    """Creates a nested search field dictionary."""

    field_values = [{'match': {'attributes.name': item['name']}}]

    if 'attribute_name' in item:
        field_values.append({'match': {'attributes.attribute_name': item['attribute_name']}})
    if 'search_type' in item:
        if item['search_type'] == 'wildcard':
            field_values.append({'wildcard': {'attributes.value': item['value']}})
        elif item['search_type'] == 'match':
            field_values.append({'match': {'attributes.value': item['value']}})
        elif item['search_type'] == 'should':
            options = []
            for option in item['value']:
                options.append({'match': {'attributes.value': option}})
            field_values.append({'bool': {'should': options}})
        elif item['search_type'] == 'must':
            options = []
            for option in item['value']:
                options.append({'match': {'attributes.value': option}})
            field_values.append({'bool': {'must': options}})

    return {
        'nested': {
            'path': item['field'],
            'query': {
                'bool': {
                    'must': field_values,
                }
            },
        }
    }


def _range(item: dict) -> dict:
    """Creates a range search field dictionary."""

    if len(item['range']) == 1:
        value = str(item['range'][0])
        if len(value) > 20:
            value = value[:19]
        if item['search_type'] == 'lte':
            return {'range': {item['field']: {'lte': int(value)}}}
        else:
            return {'range': {item['field']: {'gte': int(value)}}}
    else:
        value1 = str(item['range'][0])
        value2 = str(item['range'][1])

        if len(value1) > 20:
            value1 = value1[:19]

        if len(value2) > 20:
            value2 = value2[:19]

        return {'range': {item['field']: {'gte': int(value1), 'lte': int(value2)}}}


def _multi_values(item: dict) -> dict:
    """Creates a multi value search field dictionary."""

    options = []

    for option in item['value']:
        options.append({'term': {item['field']: option}})

    if item['search_type'] == 'should':
        return {'bool': {'should': options}}
    else:
        return {'bool': {'must': options}}


async def search(
    es_index: str, page: int, page_size: int, data: list[dict], sort_by: str = None, sort_type: str = None
):
    url = config.ELASTIC_SEARCH_SERVICE + '/{}/_search'.format(es_index)

    search_fields = []

    for item in data:
        if item['nested']:
            search_fields.append(_nested(item))
        elif item['range']:
            search_fields.append(_range(item))
        elif item['multi_values']:
            search_fields.append(_multi_values(item))
        else:
            if item['search_type'] == 'contain':
                search_fields.append({'wildcard': {item['field']: '*{}*'.format(item['value'])}})
            else:
                search_fields.append({'term': {item['field']: item['value']}})

    search_params = {
        'query': {'bool': {'must': search_fields}},
        'size': page_size,
        'from': page * page_size,
        'sort': [{sort_by: sort_type}],
    }
    __logger.info(f'elastic search url: {url}')
    __logger.info(f'elastic search params: {str(search_params)}')
    async with AsyncClient() as client:
        res = await client.request(method='GET', url=url, json=search_params)
    return res.json()
