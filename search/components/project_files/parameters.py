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

from search.components.metadata_item.models import SizeGroupBy
from search.components.parameters import QueryParameters

TIME_ZONE_REGEX = r'^[-+][0-9]{2}:[0-9]{2}$'


class ProjectFilesSizeParameters(QueryParameters):
    """Query parameters for querying project files size."""

    from_date: datetime = Query(alias='from')
    to_date: datetime = Query(alias='to')
    time_zone: str = Query(default='+00:00', regex=TIME_ZONE_REGEX)
    group_by: SizeGroupBy = Query(default=SizeGroupBy.MONTH)
