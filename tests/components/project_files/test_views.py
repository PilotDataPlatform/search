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

from search.components.item_activity.models import ItemActivityType
from search.components.metadata_item.models import MetadataItemType


class TestProjectFilesViews:
    async def test_get_project_size_usage_returns_project_storage_usage_datasets_grouped_by_zone(
        self, client, jq, metadata_item_factory
    ):
        created_metadata_item = await metadata_item_factory.create()
        from_date = (created_metadata_item.created_time - timedelta(days=1)).isoformat()
        to_date = (created_metadata_item.created_time + timedelta(days=1)).isoformat()

        response = await client.get(
            f'/v1/project-files/{created_metadata_item.container_code}/size', params={'from': from_date, 'to': to_date}
        )

        assert response.status_code == 200

        body = jq(response)
        received_zone = body('.data.datasets[].label').first()

        assert received_zone == created_metadata_item.zone

    async def test_get_project_statistics_returns_files_and_transfer_activity_statistics(
        self, fake, client, jq, metadata_item_factory, item_activity_factory
    ):
        project_code = fake.word().lower()
        time = datetime.utcnow()
        created_metadata_item = await metadata_item_factory.create(
            container_code=project_code, created_time=time, type_=MetadataItemType.FILE
        )
        await item_activity_factory.create(
            container_code=project_code, activity_time=time, activity_type=ItemActivityType.UPLOAD
        )

        expected_response = {
            'files': {
                'total_count': 1,
                'total_size': created_metadata_item.size,
            },
            'activity': {
                'today_uploaded': 1,
                'today_downloaded': 0,
            },
        }

        response = await client.get(f'/v1/project-files/{project_code}/statistics', params={'time_zone': '+00:00'})

        assert response.status_code == 200

        assert response.json() == expected_response
