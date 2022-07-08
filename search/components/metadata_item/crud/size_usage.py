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

from collections import defaultdict
from datetime import datetime
from typing import Any

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel

from search.components.metadata_item.models import MetadataItemSizeUsage
from search.components.metadata_item.models import MetadataItemSizeUsageDataset
from search.components.metadata_item.models import SizeGroupBy


class SizeUsageHandler(BaseModel):
    """Process aggregated response to provide size usage statistic.

    Only grouping by month is supported at the moment, so it's hardcoded.
    """

    from_date: datetime
    to_date: datetime
    time_zone: str
    group_by: SizeGroupBy

    @property
    def grouping_interval(self) -> str:
        return SizeGroupBy.MONTH.value

    @property
    def elasticsearch_grouping_format(self) -> str:
        return 'yyyy-MM'

    @property
    def manual_grouping_format(self) -> str:
        return '%Y-%m'

    def get_grouping_keys(self) -> list[str]:
        """Return list of keys that will be used for each bucket."""

        keys = set()
        from_date = self.from_date
        while from_date < self.to_date:
            keys.add(from_date.strftime(self.manual_grouping_format))
            from_date += relativedelta(months=1)

        return sorted(keys)

    def get_aggregations(self) -> dict[str, Any]:
        """Return aggregations to retrieve data."""

        return {
            'group_by_zone': {
                'terms': {'field': 'zone'},
                'aggs': {
                    'group_by_created_time': {
                        'date_histogram': {
                            'field': 'created_time',
                            'calendar_interval': self.grouping_interval,
                            'min_doc_count': 0,
                            'time_zone': self.time_zone,
                            'format': self.elasticsearch_grouping_format,
                            'keyed': True,
                        },
                        'aggs': {
                            'total_size': {'sum': {'field': 'size'}},
                        },
                    },
                },
            },
        }

    def process_search_result(self, result: dict[str, Any]) -> MetadataItemSizeUsage:
        """Process search result and categorize into datasets per zone."""

        buckets_by_zone = result['aggregations']['group_by_zone']['buckets']
        available_zones = {zone['key'] for zone in buckets_by_zone}

        if not available_zones:
            return MetadataItemSizeUsage(labels=[], datasets=[])

        grouping_keys = self.get_grouping_keys()

        mapping = defaultdict(dict)
        for key in grouping_keys:
            for zone in available_zones:
                mapping[key][zone] = 0

        for zone in buckets_by_zone:
            zone_key = zone['key']
            buckets_by_created_time = zone['group_by_created_time']['buckets']
            for date_key, date in buckets_by_created_time.items():
                mapping[date_key][zone_key] = int(date['total_size']['value'])

        datasets = []
        for zone in available_zones:
            values = [mapping[key][zone] for key in grouping_keys]
            datasets.append(MetadataItemSizeUsageDataset(label=zone, values=values))

        return MetadataItemSizeUsage(labels=grouping_keys, datasets=datasets)
