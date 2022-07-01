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
from pydantic import Extra


class MetadataItemAttribute(BaseModel):
    """Metadata item attribute structure."""

    name: str


class MetadataItem(BaseModel):
    """Metadata item elasticsearch document model."""

    pk: str
    id: str
    parent_path: str
    type: str
    zone: int
    name: str
    size: int
    owner: str
    container_code: str
    container_type: str
    created_time: datetime
    last_updated_time: datetime
    tags: list[str]
    template_name: str
    attributes: list[MetadataItemAttribute]
    archived: bool

    class Config:
        extra = Extra.ignore
