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
from typing import Any

from pydantic import BaseModel

from search.components.item_activity.models import ActivityGroupBy


class FileActivityHandler(BaseModel):
    """Process aggregated response to provide file activity.

    Only grouping by day is supported at the moment, so it's hardcoded.
    """

    from_date: datetime
    to_date: datetime
    time_zone: str
    group_by: ActivityGroupBy

    @property
    def grouping_interval(self) -> str:
        return ActivityGroupBy.DAY.value

    @property
    def elasticsearch_grouping_format(self) -> str:
        return 'yyyy-MM-dd'

    @property
    def manual_grouping_format(self) -> str:
        return '%Y-%m-%d'

    def get_grouping_keys(self) -> list[str]:
        """Return list of keys that will be used for each bucket."""

        keys = set()
        from_date = self.from_date
        while from_date < self.to_date:
            keys.add(from_date.strftime(self.manual_grouping_format))
            from_date += timedelta(days=1)

        return sorted(keys)

    def get_aggregations(self) -> dict[str, Any]:
        """Return aggregations to retrieve data."""

        return {
            'group_by_activity_time': {
                'date_histogram': {
                    'field': 'activity_time',
                    'calendar_interval': self.grouping_interval,
                    'min_doc_count': 0,
                    'time_zone': self.time_zone,
                    'format': self.elasticsearch_grouping_format,
                    'keyed': True,
                },
            },
        }

    def process_search_result(self, result: dict[str, Any]) -> dict[str, int]:
        """Process search result and categorize into datasets per day."""

        buckets_by_activity_time = result['aggregations']['group_by_activity_time']['buckets']
        mapping = {}

        grouping_keys = self.get_grouping_keys()
        for key in grouping_keys:
            mapping[key] = 0

        for date_key, date in buckets_by_activity_time.items():
            mapping[date_key] = date['doc_count']

        return mapping
