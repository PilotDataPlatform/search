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
from datetime import time
from datetime import timezone

import faker
import pytest


class Faker(faker.Faker):
    def date_this_year_midnight_time(self) -> datetime:
        return datetime.combine(self.date_this_year(), time(tzinfo=timezone.utc))


@pytest.fixture
def fake(pytestconfig) -> Faker:
    seed = pytestconfig.getoption('random_order_seed', '0').lstrip('default:')

    fake = Faker()
    fake.seed_instance(seed=seed)
    fake.unique.clear()

    yield fake
