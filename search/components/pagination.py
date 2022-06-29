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

import math
from typing import TypeVar

from pydantic import BaseModel
from pydantic import conint

from search.components.models import Model


class Pagination(BaseModel):
    """Base pagination control parameters."""

    page: conint(ge=1) = 1
    page_size: conint(ge=1) = 20

    @property
    def size(self) -> int:
        return self.page_size

    @property
    def from_(self) -> int:
        return self.page_size * (self.page - 1)


class Page(BaseModel):
    """Represent one page of the response."""

    pagination: Pagination
    count: int
    entries: list[Model]

    @property
    def number(self) -> int:
        return self.pagination.page

    @property
    def total_pages(self) -> int:
        return math.ceil(self.count / self.pagination.page_size)


PageType = TypeVar('PageType', bound=Page)
