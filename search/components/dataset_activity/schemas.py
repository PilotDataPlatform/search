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

from search.components.schemas import BaseSchema
from search.components.schemas import ListResponseSchema


class DatasetActivityChangeSchema(BaseSchema):
    """Dataset activity change schema."""

    property: str
    old_value: str | None
    new_value: str | None


class DatasetActivitySchema(BaseSchema):
    """Dataset activity schema."""

    activity_type: str
    activity_time: datetime
    container_code: str
    version: str | None
    target_name: str | None
    user: str
    changes: list[DatasetActivityChangeSchema]


class DatasetActivityListResponseSchema(ListResponseSchema):
    """Default schema for multiple dataset activity in response."""

    result: list[DatasetActivitySchema]
