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

from fastapi import APIRouter
from fastapi import Depends

from search.components.dataset_activity.crud import DatasetActivityCRUD
from search.components.dataset_activity.dependencies import get_dataset_activity_crud
from search.components.dataset_activity.parameters import DatasetActivityFilterParameters
from search.components.dataset_activity.parameters import DatasetActivitySortByFields
from search.components.dataset_activity.schemas import DatasetActivityListResponseSchema
from search.components.parameters import PageParameters
from search.components.parameters import SortParameters

router = APIRouter(prefix='/dataset-activity-logs', tags=['Dataset Activity'])


@router.get('/', summary='List all dataset activity logs.', response_model=DatasetActivityListResponseSchema)
async def list_dataset_activity_logs(
    filter_parameters: DatasetActivityFilterParameters = Depends(),
    sort_parameters: SortParameters.with_sort_by_fields(DatasetActivitySortByFields) = Depends(),
    page_parameters: PageParameters = Depends(),
    dataset_activity_crud: DatasetActivityCRUD = Depends(get_dataset_activity_crud),
) -> DatasetActivityListResponseSchema:
    """List dataset activity logs."""

    filtering = filter_parameters.to_filtering()
    sorting = sort_parameters.to_sorting()
    pagination = page_parameters.to_pagination()

    page = await dataset_activity_crud.list(pagination, sorting, filtering)

    response = DatasetActivityListResponseSchema.from_page(page)

    return response
