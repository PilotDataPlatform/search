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
from search.components.metadata_item.filtering import MetadataItemProjectSizeUsageFiltering
from search.components.project_files.parameters import ProjectFilesSizeParameters
from search.components.project_files.schemas import ProjectFilesSizeResponseSchema
from search.components.project_files.schemas import ProjectFilesSizeSchema

router = APIRouter(prefix='/project-files', tags=['Project Files'])


@router.get(
    '/{project_code}/size', summary='Get storage usage in the project.', response_model=ProjectFilesSizeResponseSchema
)
async def get_project_size_usage(
    project_code: str,
    parameters: ProjectFilesSizeParameters = Depends(),
    metadata_item_crud: MetadataItemCRUD = Depends(get_metadata_item_crud),
) -> ProjectFilesSizeResponseSchema:
    """Get storage usage in a project for the period."""

    filtering = MetadataItemProjectSizeUsageFiltering(
        project_code=project_code, from_date=parameters.from_date, to_date=parameters.to_date
    )

    project_size_usage = await metadata_item_crud.get_project_size_usage(
        filtering, parameters.time_zone, parameters.group_by
    )

    return ProjectFilesSizeResponseSchema(data=ProjectFilesSizeSchema(**project_size_usage.dict()))
