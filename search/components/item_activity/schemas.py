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

from search.components.item_activity.models import ItemActivityType
from search.components.models import ContainerType
from search.components.schemas import BaseSchema


class ItemActivitySchema(BaseSchema):
    """General item activity schema."""

    id: str
    activity_type: ItemActivityType
    activity_time: datetime
    container_code: str
    container_type: ContainerType
