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

from search.components.schemas import BaseSchema


class ProjectFilesSizeDatasetSchema(BaseSchema):
    """General project files size datasets schema."""

    label: int
    values: list[int]


class ProjectFilesSizeSchema(BaseSchema):
    """General project files size schema."""

    labels: list[str]
    datasets: list[ProjectFilesSizeDatasetSchema]


class ProjectFilesSizeResponseSchema(BaseSchema):
    """Default schema for project files size response."""

    data: ProjectFilesSizeSchema


class ProjectFilesTotalStatistics(BaseSchema):
    """Project files total statistics schema."""

    total_count: int
    total_size: int
    total_per_zone: dict[int, int]


class ProjectFilesTodayActivity(BaseSchema):
    """Project files today's activity schema."""

    today_uploaded: int
    today_downloaded: int


class ProjectFilesStatisticsResponseSchema(BaseSchema):
    """Default schema for project files statistics response."""

    files: ProjectFilesTotalStatistics
    activity: ProjectFilesTodayActivity


class ProjectFilesActivityResponseSchema(BaseSchema):
    """Default schema for project files activity response."""

    data: dict[str, int]
