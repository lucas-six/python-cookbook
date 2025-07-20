"""FastAPI with App."""

import asyncio
import json
import logging
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, suppress
from typing import Any, TypedDict

import aiomqtt
from fastapi import FastAPI, Request
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis

from examples.web.fastapi.routers import router
from examples.web.fastapi.settings import get_settings
from examples.web.fastapi.workers import handle_bytes

settings = get_settings()

API_DOC_STATIC_DIR = 'examples/web/fastapi/static'
API_DOC_STATIC_PATH = f'{settings.app_doc_url}/{API_DOC_STATIC_DIR}'

LOGGER = logging.getLogger('uvicorn')

MONGODB_CLIENT: AsyncIOMotorClient = AsyncIOMotorClient(str(settings.mongodb_url))
DB_XXX = MONGODB_CLIENT[settings.mongodb_db_name]
TB_XXX = DB_XXX['examples']


class State(TypedDict):
    redis_client: Redis
    mqtt_client: aiomqtt.Client


async def mqtt_listen(client: aiomqtt.Client) -> None:
    async with asyncio.TaskGroup() as tg:
        async for message in client.messages:
            msg = message.payload
            if isinstance(msg, bytes):
                tg.create_task(handle_bytes(msg), name=str(message.mid))


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[State, Any]:
    loop = asyncio.get_event_loop()

    async with (
        Redis.from_url(
            url=str(settings.redis_url),
            encoding='utf-8',
            decode_responses=True,
            max_connections=settings.cache_max_conns,
            socket_connect_timeout=settings.cache_conn_timeout,
            socket_timeout=settings.cache_timeout,
            client_name=f'python-cookbook-{os.getpid()}',
        ) as redis_client,
        aiomqtt.Client(
            settings.mqtt_host,
            settings.mqtt_port,
            username=settings.mqtt_username,
            password=settings.mqtt_password,
            timeout=settings.mqtt_timeout,
            identifier=f'python-cookbook-{os.getpid()}',
        ) as mqtt_client,
    ):
        # Subscribe MQTT
        await mqtt_client.subscribe(f'{settings.mqtt_topic_prefix}/#')
        task = loop.create_task(mqtt_listen(mqtt_client))

        app.state.redis_client = redis_client
        app.state.mqtt_client = mqtt_client

        yield {'redis_client': redis_client, 'mqtt_client': mqtt_client}

        LOGGER.debug(f'Redis client [python-cookbook-{os.getpid()}] disconected')
        LOGGER.debug(f'MQTT client [python-cookbook-{os.getpid()}] disconected')
        MONGODB_CLIENT.close()

        task.cancel()
        with suppress(asyncio.CancelledError):
            await task

    LOGGER.debug(f'Redis client [python-cookbook-{os.getpid()}] disconected')
    LOGGER.debug(f'MQTT client [python-cookbook-{os.getpid()}] disconected')
    MONGODB_CLIENT.close()


app: FastAPI = FastAPI(
    title=settings.app_name,
    docs_url=settings.app_doc_url,
    debug=settings.debug,
    openapi_url=f'{settings.app_doc_url}/openapi.json',
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)

app.mount(API_DOC_STATIC_PATH, StaticFiles(directory=API_DOC_STATIC_DIR), name='static')
assert isinstance(app.swagger_ui_oauth2_redirect_url, str)


@app.head(settings.app_doc_url, include_in_schema=False)
@app.get(settings.app_doc_url, include_in_schema=False)
async def custom_swagger_ui_html() -> HTMLResponse:
    """Custom Swagger UI"""
    assert isinstance(app.openapi_url, str)
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + ' - Swagger UI',
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url=f'{API_DOC_STATIC_PATH}/swagger-ui-bundle.js',
        swagger_css_url=f'{API_DOC_STATIC_PATH}/swagger-ui.css',
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect() -> HTMLResponse:
    """Swagger UI redirect"""
    return get_swagger_ui_oauth2_redirect_html()


@app.get(f'{settings.app_doc_url}/redoc', include_in_schema=False)
async def redoc_html() -> HTMLResponse:
    """Custom redoc html."""
    assert isinstance(app.openapi_url, str)
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + ' - ReDoc',
        redoc_js_url=f'{API_DOC_STATIC_PATH}/redoc.standalone.js',
    )


@app.get('/api')
async def root(request: Request) -> dict[str, str | None]:
    db_doc = await TB_XXX.find_one({'name': settings.app_name})
    cache_val = await request.state.redis_client.get(f'{settings.cache_prefix}:examples')
    await request.state.mqtt_client.publish(
        f'{settings.mqtt_topic_prefix}/example',
        payload=json.dumps({'msg': 'hello'}, ensure_ascii=False),
        qos=settings.mqtt_qos,
    )
    return {'db': db_doc, 'cache': cache_val}


app.include_router(router, prefix='/api/router', tags=['router'])
