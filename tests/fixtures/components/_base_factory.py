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
from typing import get_args

from faker import Faker

from search.components.crud import CRUD
from search.components.models import Model


class BaseFactory:
    """Base class for creating testing purpose entries."""

    crud: CRUD
    fake: Faker

    def __init__(self, crud: CRUD, fake: Faker) -> None:
        self.crud = crud
        self.fake = fake

    def _generate_mappings_for_model(self, model: Model) -> dict[str, Any]:
        properties = {}

        for name, field in model.__annotations__.items():
            if name == 'pk':
                continue

            if str not in get_args(field):
                continue

            properties[name] = {
                'type': 'text',
                'fields': {
                    # Allow sorting using keyword on text fields
                    # https://www.elastic.co/guide/en/elasticsearch/reference/7.17/text.html#before-enabling-fielddata
                    'keyword': {
                        'type': 'keyword',
                    }
                },
            }

        return {
            'properties': properties,
        }

    async def create_index(self) -> None:
        """Create a new index."""

        mappings = self._generate_mappings_for_model(self.crud.model)

        await self.crud.client.indices.create(index=self.crud.index, mappings=mappings)

    async def delete_index(self) -> None:
        """Remove an existing index."""

        await self.crud.client.indices.delete(index=self.crud.index)
