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

pytest_plugins = [
    'tests.fixtures.components.dataset_activity',
    'tests.fixtures.components.item_activity',
    'tests.fixtures.components.metadata_item',
    'tests.fixtures.app',
    'tests.fixtures.elasticsearch',
    'tests.fixtures.fake',
    'tests.fixtures.jq',
]
