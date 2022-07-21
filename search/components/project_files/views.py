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

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from search.components.item_activity.crud import ItemActivityCRUD
from search.components.item_activity.dependencies import get_item_activity_crud
from search.components.item_activity.filtering import ItemActivityProjectFileActivityFiltering
from search.components.metadata_item.crud import MetadataItemCRUD
from search.components.metadata_item.dependencies import get_metadata_item_crud
from search.components.metadata_item.filtering import MetadataItemProjectSizeUsageFiltering
from search.components.project_files.parameters import TIME_ZONE_REGEX
from search.components.project_files.parameters import ProjectFilesActivityParameters
from search.components.project_files.parameters import ProjectFilesSizeParameters
from search.components.project_files.schemas import ProjectFilesActivityResponseSchema
from search.components.project_files.schemas import ProjectFilesSizeResponseSchema
from search.components.project_files.schemas import ProjectFilesSizeSchema
from search.components.project_files.schemas import ProjectFilesStatisticsResponseSchema
from search.components.project_files.schemas import ProjectFilesTodayActivity
from search.components.project_files.schemas import ProjectFilesTotalStatistics

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


@router.get(
    '/{project_code}/statistics',
    summary='Get files and transfer activity statistics in the project.',
    response_model=ProjectFilesStatisticsResponseSchema,
)
async def get_project_statistics(
    project_code: str,
    time_zone: str = Query(default='+00:00', regex=TIME_ZONE_REGEX),
    metadata_item_crud: MetadataItemCRUD = Depends(get_metadata_item_crud),
    item_activity_crud: ItemActivityCRUD = Depends(get_item_activity_crud),
) -> ProjectFilesStatisticsResponseSchema:
    """Get files and transfer activity statistics in a project for the period."""

    now = datetime.utcnow()

    statistics = await metadata_item_crud.get_project_statistics(project_code)
    transfer_statistics = await item_activity_crud.get_project_transfer_statistics(project_code, now, time_zone)

    return ProjectFilesStatisticsResponseSchema(
        files=ProjectFilesTotalStatistics(
            total_count=statistics.count,
            total_size=statistics.size,
            total_per_zone=statistics.count_by_zone,
        ),
        activity=ProjectFilesTodayActivity(
            today_uploaded=transfer_statistics.uploaded,
            today_downloaded=transfer_statistics.downloaded,
        ),
    )


@router.get(
    '/{project_code}/activity',
    summary='Get file activity in the project.',
    response_model=ProjectFilesActivityResponseSchema,
)
async def get_project_file_activity(
    project_code: str,
    parameters: ProjectFilesActivityParameters = Depends(),
    item_activity_crud: ItemActivityCRUD = Depends(get_item_activity_crud),
) -> ProjectFilesActivityResponseSchema:
    """Get file activity in a project for the period."""

    filtering = ItemActivityProjectFileActivityFiltering(
        project_code=project_code,
        activity_type=parameters.activity_type,
        from_date=parameters.from_date,
        to_date=parameters.to_date,
    )

    project_file_activity = await item_activity_crud.get_project_file_activity(
        filtering, parameters.time_zone, parameters.group_by
    )

    return ProjectFilesActivityResponseSchema(data=project_file_activity)
