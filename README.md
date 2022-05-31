# Search Service

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg?style=for-the-badge)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.10](https://img.shields.io/badge/python-3.10-brightgreen?style=for-the-badge)](https://www.python.org/)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/PilotDataPlatform/search/ci?style=for-the-badge)](https://github.com/PilotDataPlatform/search/actions)
[![codecov](https://img.shields.io/codecov/c/github/PilotDataPlatform/search?style=for-the-badge)](https://codecov.io/gh/PilotDataPlatform/search)

## About

Service for performing searches.

### Start

1. Install [Docker](https://www.docker.com/get-started/).
2. Start container with search application.

       docker compose up

3. Visit http://127.0.0.1:5064/v1/api-doc for API documentation.

### Development

1. Install [Poetry](https://python-poetry.org/docs/#installation).
2. Install dependencies.

       poetry install

3. Add environment variables into `.env`.
4. Run application.

       poetry run python -m search
