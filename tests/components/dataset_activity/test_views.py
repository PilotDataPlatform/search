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


class TestDatasetActivityLogsViews:
    async def test_list_dataset_activity_returns_list_of_existing_dataset_activities(
        self, client, jq, dataset_activity_factory
    ):
        await dataset_activity_factory.bulk_create(3)

        response = await client.get('/v1/dataset-activity-logs/')

        assert response.status_code == 200

        body = jq(response)
        received_total = body('.total').first()

        assert received_total == 3

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
    async def test_list_dataset_activity_returns_properly_paginated_response(
        self, items_number, page, page_size, expected_count, client, jq, dataset_activity_factory
    ):
        await dataset_activity_factory.bulk_create(items_number)

        response = await client.get('/v1/dataset-activity-logs/', params={'page': page, 'page_size': page_size})

        assert response.status_code == 200

        body = jq(response)
        received_dataset_activity_logs_cc = body('.result[].container_code').all()
        received_total = body('.total').first()

        assert len(received_dataset_activity_logs_cc) == expected_count
        assert received_total == items_number

    @pytest.mark.parametrize('parameter', ['version', 'target_name', 'user'])
    async def test_list_dataset_activities_returns_dataset_activity_filtered_by_parameter_full_text_match(
        self, parameter, client, jq, dataset_activity_factory
    ):
        created_dataset_activity = await dataset_activity_factory.bulk_create(3)
        dataset_activity = created_dataset_activity.pop()

        response = await client.get(
            '/v1/dataset-activity-logs/', params={parameter: getattr(dataset_activity, parameter)}
        )

        body = jq(response)
        received_ccs = body('.result[].container_code').all()
        received_total = body('.total').first()

        assert received_ccs == [dataset_activity.container_code]
        assert received_total == 1

    @pytest.mark.parametrize('parameter', ['version', 'target_name', 'user'])
    async def test_list_dataset_activities_returns_dataset_activity_filtered_by_parameter_partial_match(
        self, parameter, client, jq, fake, dataset_activity_factory
    ):
        created_dataset_activities = await dataset_activity_factory.bulk_create(3)
        dataset_activity = created_dataset_activities.pop()
        value = getattr(dataset_activity, parameter)
        lookup = value.replace(value[5:], '%')

        response = await client.get('/v1/dataset-activity-logs/', params={parameter: lookup})

        body = jq(response)
        received_ccs = body('.result[].container_code').all()
        received_total = body('.total').first()

        assert received_ccs == [dataset_activity.container_code]
        assert received_total == 1

    @pytest.mark.parametrize('parameter', ['activity_type', 'container_code'])
    async def test_list_dataset_activities_returns_dataset_activity_filtered_by_parameter_match(
        self, parameter, client, jq, fake, dataset_activity_factory
    ):
        created_dataset_activities = await dataset_activity_factory.bulk_create(3)
        value = getattr(created_dataset_activities[0], parameter)
        expected_ccs = {item.container_code for item in created_dataset_activities if getattr(item, parameter) == value}

        response = await client.get('/v1/dataset-activity-logs/', params={parameter: value})

        body = jq(response)
        received_ccs = body('.result[].container_code').all()
        received_total = body('.total').first()

        assert set(received_ccs) == expected_ccs
        assert received_total == len(expected_ccs)

    async def test_list_dataset_activities_returns_dataset_activities_filtered_by_activity_time_parameters(
        self, client, jq, fake, dataset_activity_factory
    ):
        today = datetime.utcnow()
        week_ago = today - timedelta(days=7)
        two_weeks_ago = today - timedelta(days=14)

        [
            await dataset_activity_factory.create(activity_time=fake.date_time_between_dates(two_weeks_ago, week_ago))
            for _ in range(2)
        ]
        dataset_activity = await dataset_activity_factory.create(
            activity_time=fake.date_time_between_dates(week_ago, today)
        )

        params = {
            'activity_time_start': int(datetime.timestamp(week_ago)),
            'activity_time_end': int(datetime.timestamp(today)),
        }
        response = await client.get('/v1/dataset-activity-logs/', params=params)

        body = jq(response)
        received_ccs = body('.result[].container_code').all()
        received_total = body('.total').first()

        assert received_ccs == [str(dataset_activity.container_code)]
        assert received_total == 1
