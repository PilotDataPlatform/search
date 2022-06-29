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

from search.components.metadata_item.crud import MetadataItemCRUD
from search.components.metadata_item.dependencies import get_metadata_item_crud
from search.components.metadata_item.parameters import MetadataItemFilterParameters
from search.components.metadata_item.parameters import MetadataItemSortByFields
from search.components.metadata_item.schemas import MetadataItemListResponseSchema
from search.components.parameters import PageParameters
from search.components.parameters import SortParameters

router = APIRouter(prefix='/metadata-items', tags=['Metadata Items'])


@router.get('/', summary='List all metadata items.', response_model=MetadataItemListResponseSchema)
async def list_metadata_items(
    filter_parameters: MetadataItemFilterParameters = Depends(),
    sort_parameters: SortParameters.with_sort_by_fields(MetadataItemSortByFields) = Depends(),
    page_parameters: PageParameters = Depends(),
    metadata_item_crud: MetadataItemCRUD = Depends(get_metadata_item_crud),
) -> MetadataItemListResponseSchema:
    """List metadata items."""

    filtering = filter_parameters.to_filtering()
    sorting = sort_parameters.to_sorting()
    pagination = page_parameters.to_pagination()

    page = await metadata_item_crud.list(pagination, sorting, filtering)

    response = MetadataItemListResponseSchema.from_page(page)

    return response
