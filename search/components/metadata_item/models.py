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


class SizeGroupBy(StrEnum):
    """Store possible group by options for metadata items."""

    MONTH = 'month'


class MetadataItemType(StrEnum):
    """Store all metadata item types."""

    FILE = 'file'
    FOLDER = 'folder'


class MetadataItemAttribute(BaseModel):
    """Metadata item attribute structure."""

    name: str


class MetadataItem(BaseModel):
    """Metadata item elasticsearch document model."""

    pk: str
    id: str
    parent_path: str | None
    type: str
    zone: int
    name: str
    size: int
    owner: str
    container_code: str
    container_type: ContainerType
    created_time: datetime
    last_updated_time: datetime
    tags: list[str]
    template_name: str
    attributes: list[MetadataItemAttribute]
    archived: bool


class MetadataItemSizeUsageDataset(BaseModel):
    """Metadata item size usage dataset structure."""

    label: int
    values: list[int]


class MetadataItemSizeUsage(BaseModel):
    """Metadata item size usage model."""

    labels: list[str]
    datasets: list[MetadataItemSizeUsageDataset]


class MetadataItemSizeStatistics(BaseModel):
    """Metadata item size statistics model."""

    count: int
    size: int
