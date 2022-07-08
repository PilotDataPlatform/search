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

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from search.components.item_activity.crud import ItemActivityCRUD
from search.dependencies import get_elasticsearch_client


def get_item_activity_crud(
    elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client),
) -> ItemActivityCRUD:
    """Return an instance of ItemActivityCRUD as a dependency."""

    return ItemActivityCRUD(elasticsearch_client)
