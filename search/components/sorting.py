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

from typing import Any

from pydantic import BaseModel

from search.components.types import StrEnum


class SortingOrder(StrEnum):
    """Available sorting orders."""

    ASC = 'asc'
    DESC = 'desc'


class Sorting(BaseModel):
    """Base sorting control parameters."""

    field: str | None = None
    order: SortingOrder

    def __bool__(self) -> bool:
        """Sorting considered valid when the field is specified."""

        return self.field is not None

    def apply(self) -> list[dict[str, Any]]:
        """Return sorting field with applied ordering that will be used as sort parameter."""

        return [{self.field: self.order.value}]
