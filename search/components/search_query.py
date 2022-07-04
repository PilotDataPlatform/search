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


class SearchQuery:
    """Build elastic search query."""

    def __init__(self) -> None:
        self.must = []

    def match_keyword(self, field: str, value: str) -> None:
        query_type = 'match'

        is_wildcard = '%' in value
        if is_wildcard:
            query_type = 'wildcard'
            value = value.replace('%', '*')

        self.must.append({query_type: {field: value}})

    def match_range(self, field: str, **kwds: Any) -> None:
        self.must.append({'range': {field: kwds}})

    def match_term(self, field: str, value: str | int | bool) -> None:
        self.must.append({'term': {field: value}})

    def build(self) -> dict[str, Any]:
        if not self.must:
            return {'match_all': {}}

        return {'bool': {'must': self.must}}
