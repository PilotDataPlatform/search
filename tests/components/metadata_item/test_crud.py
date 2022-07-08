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

from dateutil.relativedelta import relativedelta

from search.components.metadata_item.filtering import MetadataItemProjectSizeUsageFiltering
from search.components.metadata_item.models import MetadataItemSizeStatistics
from search.components.metadata_item.models import MetadataItemSizeUsage
from search.components.metadata_item.models import MetadataItemSizeUsageDataset
from search.components.metadata_item.models import MetadataItemType
from search.components.metadata_item.models import SizeGroupBy


class TestMetadataItemCRUD:
    async def test_get_project_size_usage_returns_project_storage_usage_datasets_grouped_by_zone(
        self, fake, metadata_item_crud, metadata_item_factory
    ):
        to_date = fake.date_this_year_midnight_time()
        from_date = to_date - relativedelta(years=1)
        project_code = fake.word().lower()
        expected_datasets = {}

        for month in range(12):
            created_time = from_date + relativedelta(months=month)
            for zone in [0, 1]:
                created_metadata_item = await metadata_item_factory.create(
                    created_time=created_time, container_code=project_code, zone=zone
                )
                zone_dataset = expected_datasets.setdefault(zone, MetadataItemSizeUsageDataset(label=zone, values=[]))
                zone_dataset.values.append(created_metadata_item.size)

        filtering = MetadataItemProjectSizeUsageFiltering(
            project_code=project_code, from_date=from_date, to_date=to_date
        )
        result = await metadata_item_crud.get_project_size_usage(filtering, '+00:00', SizeGroupBy.MONTH)

        assert len(result.datasets) == 2
        assert result.datasets == list(expected_datasets.values())

    async def test_get_project_size_usage_returns_project_storage_usage_datasets_considering_time_zone_offset(
        self, fake, metadata_item_crud, metadata_item_factory
    ):
        to_date = fake.date_this_year_midnight_time().replace(day=1)
        from_date = to_date - relativedelta(months=2)
        project_code = fake.word().lower()
        created_time = from_date + relativedelta(months=1, hours=1)
        created_metadata_item = await metadata_item_factory.create(
            created_time=created_time, container_code=project_code
        )

        filtering = MetadataItemProjectSizeUsageFiltering(
            project_code=project_code, from_date=from_date, to_date=to_date
        )
        utc_result = await metadata_item_crud.get_project_size_usage(filtering, '+00:00', SizeGroupBy.MONTH)
        est_result = await metadata_item_crud.get_project_size_usage(filtering, '-05:00', SizeGroupBy.MONTH)

        assert utc_result.datasets[0].values == [0, created_metadata_item.size]
        assert est_result.datasets[0].values == [created_metadata_item.size, 0]

    async def test_get_project_size_usage_returns_datasets_with_zero_values_for_dates_without_entries(
        self, fake, metadata_item_crud, metadata_item_factory
    ):
        to_date = fake.date_this_year_midnight_time()
        from_date = to_date - relativedelta(years=1)
        project_code = fake.word().lower()
        created_metadata_item = await metadata_item_factory.create(
            created_time=from_date, container_code=project_code, zone=0
        )
        expected_dataset_values = [created_metadata_item.size] + [0] * 11

        filtering = MetadataItemProjectSizeUsageFiltering(
            project_code=project_code, from_date=from_date, to_date=to_date
        )
        result = await metadata_item_crud.get_project_size_usage(filtering, '+00:00', SizeGroupBy.MONTH)

        assert len(result.datasets) == 1
        assert result.datasets[0].values == expected_dataset_values

    async def test_get_project_size_usage_returns_datasets_with_months_in_labels(
        self, fake, metadata_item_crud, metadata_item_factory
    ):
        to_date = fake.date_this_year_midnight_time()
        from_date = to_date - relativedelta(years=2)
        project_code = fake.word().lower()
        await metadata_item_factory.create(created_time=from_date, container_code=project_code)
        expected_labels = []

        start_date = from_date
        while start_date < to_date:
            expected_labels.append(start_date.strftime('%Y-%m'))
            start_date += relativedelta(months=1)

        filtering = MetadataItemProjectSizeUsageFiltering(
            project_code=project_code, from_date=from_date, to_date=to_date
        )
        result = await metadata_item_crud.get_project_size_usage(filtering, '+00:00', SizeGroupBy.MONTH)

        assert len(result.datasets) == 1
        assert result.labels == expected_labels

    async def test_get_project_size_usage_returns_empty_size_usage_when_no_entries_for_zones_are_available(
        self, fake, metadata_item_crud, metadata_item_factory
    ):
        to_date = fake.date_this_year_midnight_time()
        from_date = to_date - relativedelta(months=1)
        project_code = fake.word().lower()

        filtering = MetadataItemProjectSizeUsageFiltering(
            project_code=project_code, from_date=from_date, to_date=to_date
        )
        result = await metadata_item_crud.get_project_size_usage(filtering, '+00:00', SizeGroupBy.MONTH)

        assert result == MetadataItemSizeUsage(labels=[], datasets=[])

    async def test_get_project_statistics_returns_total_count_and_size(
        self, fake, metadata_item_crud, metadata_item_factory
    ):
        project_code = fake.word().lower()
        created_metadata_items = await metadata_item_factory.bulk_create(
            3, type_=MetadataItemType.FILE, container_code=project_code, size=fake.pyint(1024**2, 1024**3)
        )
        expected_size = sum(item.size for item in created_metadata_items)

        result = await metadata_item_crud.get_project_statistics(project_code)

        assert result == MetadataItemSizeStatistics(count=3, size=expected_size)
