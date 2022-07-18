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

from datetime import timedelta
from datetime import timezone

from search.components.item_activity.filtering import ItemActivityProjectFileActivityFiltering
from search.components.item_activity.models import ActivityGroupBy
from search.components.item_activity.models import ItemActivityTransferStatistics
from search.components.item_activity.models import ItemActivityType
from search.components.models import ContainerType


class TestItemActivityCRUD:
    async def test_get_project_transfer_statistics_returns_valid_stats_considering_activity_time(
        self, fake, item_activity_crud, item_activity_factory
    ):
        project_code = fake.word().lower()
        activity_time = fake.past_datetime(tzinfo=timezone.utc).replace(hour=12)
        for activity_type in [ItemActivityType.DOWNLOAD, ItemActivityType.UPLOAD]:
            await item_activity_factory.bulk_create(
                2, container_code=project_code, activity_time=activity_time, activity_type=activity_type
            )

        received_transfer_statistics = await item_activity_crud.get_project_transfer_statistics(
            project_code, activity_time, '+00:00'
        )

        assert received_transfer_statistics == ItemActivityTransferStatistics(uploaded=2, downloaded=2)

    async def test_get_project_transfer_statistics_returns_valid_stats_considering_activity_time_and_time_zone(
        self, fake, item_activity_crud, item_activity_factory
    ):
        project_code = fake.word().lower()
        activity_time = fake.past_datetime(tzinfo=timezone.utc).replace(hour=22)
        for hours in range(0, 9, 3):
            await item_activity_factory.create(
                container_code=project_code,
                activity_time=activity_time + timedelta(hours=hours),
                activity_type=ItemActivityType.DOWNLOAD,
            )

        received_transfer_statistics = await item_activity_crud.get_project_transfer_statistics(
            project_code, activity_time, '+05:00'
        )

        assert received_transfer_statistics == ItemActivityTransferStatistics(uploaded=0, downloaded=2)

    async def test_get_project_file_activity_returns_project_activity_grouped_by_day(
        self, fake, item_activity_crud, item_activity_factory
    ):
        to_date = fake.past_datetime(tzinfo=timezone.utc)
        from_date = to_date - timedelta(days=3)
        project_code = fake.word().lower()
        expected_file_activity = {}

        for day in range(3):
            activity_time = from_date + timedelta(days=day)
            created_item_activity = await item_activity_factory.create(
                container_type=ContainerType.PROJECT, container_code=project_code, activity_time=activity_time
            )
            key = activity_time.strftime('%Y-%m-%d')
            value = 1 if created_item_activity.activity_type == ItemActivityType.DOWNLOAD else 0
            expected_file_activity[key] = value

        filtering = ItemActivityProjectFileActivityFiltering(
            project_code=project_code, activity_type=ItemActivityType.DOWNLOAD, from_date=from_date, to_date=to_date
        )
        received_file_activity = await item_activity_crud.get_project_file_activity(
            filtering, '+00:00', ActivityGroupBy.DAY
        )

        assert received_file_activity == expected_file_activity
