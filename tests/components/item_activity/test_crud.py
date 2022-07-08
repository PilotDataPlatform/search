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

from datetime import timezone

from search.components.item_activity.models import ItemActivityTransferStatistics
from search.components.item_activity.models import ItemActivityType


class TestItemActivityCRUD:
    async def test_get_project_transfer_statistics_returns_valid_stats_considering_activity_time(
        self, fake, item_activity_crud, item_activity_factory
    ):
        project_code = fake.word().lower()
        activity_time = fake.past_datetime(tzinfo=timezone.utc).replace(hour=12)
        for activity_type in [ItemActivityType.DOWNLOAD, ItemActivityType.UPLOAD]:
            await item_activity_factory.create(
                container_code=project_code, activity_time=activity_time, activity_type=activity_type
            )

        received_transfer_statistics = await item_activity_crud.get_project_transfer_statistics(
            project_code, activity_time, '+00:00'
        )

        assert received_transfer_statistics == ItemActivityTransferStatistics(uploaded=1, downloaded=1)
