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

from pydantic import BaseModel

from search.components.search_query import SearchQuery


class Filtering(BaseModel):
    """Base filtering control parameters."""

    def __bool__(self) -> bool:
        """Filtering considered valid when at least one attribute has a value."""

        values = self.dict()

        for name in self.__fields__.keys():
            if values[name] is not None:
                return True

        return False

    def apply(self, search_query: SearchQuery) -> None:
        """Add filtering into search query."""

        raise NotImplementedError
