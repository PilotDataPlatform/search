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

from functools import partial

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from search.components.activity_logs import activity_logs_router
from search.components.exceptions import ServiceException
from search.components.exceptions import UnhandledException
from search.components.metadata_items import metadata_item_router
from search.config import Settings
from search.config import get_settings


def create_app() -> FastAPI:
    """Initialize and configure the application."""

    settings = get_settings()

    app = FastAPI(
        title='Search Service',
        description='Service for performing searches.',
        docs_url='/v1/api-doc',
        redoc_url='/v1/api-redoc',
        version=settings.VERSION,
    )

    setup_routers(app)
    setup_middlewares(app, settings)
    setup_dependencies(app, settings)
    setup_exception_handlers(app)
    setup_tracing(app, settings)

    return app


def setup_routers(app: FastAPI) -> None:
    """Configure the application routers."""

    app.include_router(metadata_item_router, prefix='/v1')
    app.include_router(activity_logs_router, prefix='/v1')


def setup_middlewares(app: FastAPI, settings: Settings) -> None:
    """Configure the application middlewares."""

    app.add_middleware(
        CORSMiddleware,
        allow_origins='*',
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def setup_dependencies(app: FastAPI, settings: Settings) -> None:
    """Perform dependencies setup/teardown at the application startup/shutdown events."""

    app.add_event_handler('startup', partial(startup_event, settings))


async def startup_event(settings: Settings) -> None:
    """Initialise dependencies at the application startup event."""


def setup_exception_handlers(app: FastAPI) -> None:
    """Configure the application exception handlers."""

    app.add_exception_handler(ServiceException, service_exception_handler)
    app.add_exception_handler(Exception, unexpected_exception_handler)


def service_exception_handler(request: Request, exception: ServiceException) -> JSONResponse:
    """Return the default response structure for service exceptions."""

    return JSONResponse(status_code=exception.status, content={'error': exception.dict()})


def unexpected_exception_handler(request: Request, exception: Exception) -> JSONResponse:
    """Return the default unhandled exception response structure for all unexpected exceptions."""

    return service_exception_handler(request, UnhandledException())


def setup_tracing(app: FastAPI, settings: Settings) -> None:
    """Instrument the application with OpenTelemetry tracing."""

    if not settings.OPEN_TELEMETRY_ENABLED:
        return

    tracer_provider = TracerProvider(resource=Resource.create({SERVICE_NAME: settings.APP_NAME}))
    trace.set_tracer_provider(tracer_provider)

    FastAPIInstrumentor.instrument_app(app)

    jaeger_exporter = JaegerExporter(
        agent_host_name=settings.OPEN_TELEMETRY_HOST, agent_port=settings.OPEN_TELEMETRY_PORT
    )

    tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
