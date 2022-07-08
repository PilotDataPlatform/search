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

from search.components.models import ModelList


class TestModelList:
    def test_map_by_field_returns_map_based_on_field_argument_as_key(self, fake):
        class Model(BaseModel):
            id: int

        model_1 = Model(id=fake.pyint())
        model_2 = Model(id=fake.pyint())

        models = ModelList([model_1, model_2])

        expected_map = {
            str(model_1.id): model_1,
            str(model_2.id): model_2,
        }

        assert models.map_by_field('id', str) == expected_map

    def test_get_field_values_returns_list_with_values_each_model_has_in_field_attribute(self, fake):
        class Model(BaseModel):
            key: str

        model_1 = Model(key=fake.word())
        model_2 = Model(key=fake.word())

        models = ModelList([model_1, model_2])

        expected_list = [model_1.key, model_2.key]

        assert models.get_field_values('key') == expected_list
