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

from fastapi import Query

from search.components.dataset_activity.filtering import DatasetActivityFiltering
from search.components.parameters import FilterParameters
from search.components.parameters import SortByFields


class DatasetActivitySortByFields(SortByFields):
    """Fields by which dataset activity logs can be sorted."""

    ACTIVITY_TIME = 'activity_time'


class DatasetActivityFilterParameters(FilterParameters):
    """Query parameters for dataset activity filtering."""

    activity_type: str | None = Query(default=None)
    activity_time_start: datetime | None = Query(default=None)
    activity_time_end: datetime | None = Query(default=None)
    container_code: str | None = Query(default=None)
    version: str | None = Query(default=None)
    target_name: str | None = Query(default=None)
    user: str | None = Query(default=None)

    def to_filtering(self) -> DatasetActivityFiltering:
        return DatasetActivityFiltering(
            activity_type=self.activity_type,
            activity_time_start=self.activity_time_start,
            activity_time_end=self.activity_time_end,
            container_code=self.container_code,
            version=self.version,
            target_name=self.target_name,
            user=self.user,
        )
