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
from datetime import timedelta

import pytest

from search.components.metadata_item.parameters import MetadataItemSortByFields
from search.components.sorting import SortingOrder


class TestMetadataItemViews:
    async def test_list_metadata_items_returns_list_of_existing_metadata_items(self, client, jq, metadata_item_factory):
        created_metadata_item = await metadata_item_factory.create()

        response = await client.get('/v1/metadata-items/')

        assert response.status_code == 200

        body = jq(response)
        received_metadata_item_pk = body('.result[].pk').first()
        received_total = body('.total').first()

        assert received_metadata_item_pk == str(created_metadata_item.pk)
        assert received_total == 1

    @pytest.mark.parametrize(
        'items_number,page,page_size,expected_count',
        [
            (4, 1, 3, 3),
            (4, 2, 3, 1),
            (2, 1, 3, 2),
            (2, 2, 1, 1),
            (2, 3, 1, 0),
        ],
    )
    async def test_list_metadata_items_returns_properly_paginated_response(
        self, items_number, page, page_size, expected_count, client, jq, metadata_item_factory
    ):
        await metadata_item_factory.bulk_create(items_number)

        response = await client.get('/v1/metadata-items/', params={'page': page, 'page_size': page_size})

        assert response.status_code == 200

        body = jq(response)
        received_metadata_item_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert len(received_metadata_item_ids) == expected_count
        assert received_total == items_number

    @pytest.mark.parametrize('sort_by', MetadataItemSortByFields.values())
    @pytest.mark.parametrize('sort_order', SortingOrder.values())
    async def test_list_metadata_items_returns_results_sorted_by_field_with_proper_order(
        self, sort_by, sort_order, client, jq, metadata_item_factory
    ):
        created_metadata_items = await metadata_item_factory.bulk_create(3)
        field_values = created_metadata_items.get_field_values(sort_by)
        if sort_by in ('created_time', 'last_updated_time'):
            field_values = [key.isoformat() for key in field_values]
        expected_values = sorted(field_values, reverse=sort_order == SortingOrder.DESC)

        response = await client.get('/v1/metadata-items/', params={'sort_by': sort_by, 'sort_order': sort_order})

        body = jq(response)
        received_values = body(f'.result[].{sort_by}').all()
        received_total = body('.total').first()

        assert received_values == expected_values
        assert received_total == 3

    @pytest.mark.parametrize('parameter', ['name', 'owner'])
    async def test_list_metadata_items_returns_metadata_item_filtered_by_parameter_full_text_match(
        self, parameter, client, jq, metadata_item_factory
    ):
        created_metadata_items = await metadata_item_factory.bulk_create(3)
        metadata_item = created_metadata_items.pop()

        response = await client.get('/v1/metadata-items/', params={parameter: getattr(metadata_item, parameter)})

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert received_ids == [str(metadata_item.id)]
        assert received_total == 1

    @pytest.mark.parametrize('parameter', ['name', 'owner'])
    async def test_list_metadata_items_returns_metadata_item_filtered_by_parameter_partial_match(
        self, parameter, client, jq, fake, metadata_item_factory
    ):
        created_metadata_items = await metadata_item_factory.bulk_create(3)
        metadata_item = created_metadata_items.pop()
        value = getattr(metadata_item, parameter)
        lookup = value.replace(value[5:], '%')

        response = await client.get('/v1/metadata-items/', params={parameter: lookup})

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert received_ids == [str(metadata_item.id)]
        assert received_total == 1

    @pytest.mark.parametrize('parameter', ['zone', 'container_code', 'container_type'])
    async def test_list_metadata_items_returns_metadata_item_filtered_by_parameter_match(
        self, parameter, client, jq, fake, metadata_item_factory
    ):
        created_metadata_items = await metadata_item_factory.bulk_create(3)
        value = getattr(created_metadata_items[0], parameter)
        expected_ids = {item.id for item in created_metadata_items if getattr(item, parameter) == value}

        response = await client.get('/v1/metadata-items/', params={parameter: value})

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert set(received_ids) == expected_ids
        assert received_total == len(expected_ids)

    async def test_list_metadata_items_returns_metadata_items_filtered_by_created_time_parameters(
        self, client, jq, fake, metadata_item_factory
    ):
        today = datetime.utcnow()
        week_ago = today - timedelta(days=7)
        two_weeks_ago = today - timedelta(days=14)

        [
            await metadata_item_factory.create(created_time=fake.date_time_between_dates(two_weeks_ago, week_ago))
            for _ in range(2)
        ]
        metadata_item = await metadata_item_factory.create(created_time=fake.date_time_between_dates(week_ago, today))

        params = {
            'created_time_start': int(datetime.timestamp(week_ago)),
            'created_time_end': int(datetime.timestamp(today)),
        }
        response = await client.get('/v1/metadata-items/', params=params)

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert received_ids == [str(metadata_item.id)]
        assert received_total == 1

    async def test_list_metadata_items_returns_metadata_items_filtered_by_size_parameters(
        self, client, jq, fake, metadata_item_factory
    ):
        size_10mb = 10 * 1024**2
        size_100mb = 100 * 1024**2
        size_1gb = 1024**3

        [await metadata_item_factory.create(size=fake.pyint(size_10mb, size_100mb)) for _ in range(2)]
        metadata_item = await metadata_item_factory.create(size=fake.pyint(size_100mb, size_1gb))

        params = {
            'size_gte': size_100mb,
            'size_lte': size_1gb,
        }
        response = await client.get('/v1/metadata-items/', params=params)

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert received_ids == [str(metadata_item.id)]
        assert received_total == 1

    @pytest.mark.parametrize('is_archived', [True, False])
    async def test_list_metadata_items_returns_metadata_items_filtered_by_value_in_is_archived_parameter(
        self, is_archived, client, jq, metadata_item_factory
    ):
        await metadata_item_factory.bulk_create(2, archived=not is_archived)
        created_metadata_items = await metadata_item_factory.bulk_create(2, archived=is_archived)
        mapping = created_metadata_items.map_by_field('id', str)
        expected_ids = list(mapping.keys())

        response = await client.get('/v1/metadata-items/', params={'is_archived': str(is_archived).lower()})

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert set(received_ids) == set(expected_ids)
        assert received_total == 2

    async def test_list_metadata_items_returns_total_per_zone_attribute_with_count_of_documents_in_each_zone(
        self, client, jq, metadata_item_factory
    ):
        expected_total_per_zone = {}
        for zone in range(3):
            await metadata_item_factory.create(zone=zone)
            expected_total_per_zone[str(zone)] = 1

        response = await client.get('/v1/metadata-items/')

        body = jq(response)
        received_total_per_zone = body('.total_per_zone').first()

        assert received_total_per_zone == expected_total_per_zone
