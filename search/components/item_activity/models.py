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

from pydantic import BaseModel

from search.components.models import ContainerType
from search.components.types import StrEnum


class ActivityGroupBy(StrEnum):
    """Store possible group by options for item activities."""

    DAY = 'day'


class ItemActivityType(StrEnum):
    """Store all available item activity types."""

    DOWNLOAD = 'download'
    UPLOAD = 'upload'
    DELETE = 'delete'
    COPY = 'copy'


class ItemActivity(BaseModel):
    """Item activity elasticsearch document model."""

    pk: str
    id: str
    activity_type: ItemActivityType
    activity_time: datetime
    container_code: str
    container_type: ContainerType


class ItemActivityTransferStatistics(BaseModel):
    """Item activity transfer statistics model."""

    uploaded: int
    downloaded: int
