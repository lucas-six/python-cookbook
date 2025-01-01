# `FastAPI` App

## Installation

### `motor`

See [MongoDB **`motor`** - Python Cookbook](../../system_services/mongodb_motor)

### ODM (Object-Document Model): `beanie`, `pyodmongo`

```bash
pipenv install beanie
pipenv install pyodmongo
```

```toml
# pyproject.toml

dependencies = [
    "beanie",
    "pyodmongo",
]
```

## App

### `.env`

```ini
# .env

APP_NAME="FastAPI App"
APP_VERSION="v0.0.1"
APP_DESCRIPTION="FastAPI app description."
DEBUG=true
MONGODB_URL="mongodb://localhost:27019/?replicaSet=xxx&maxPoolSize=4096&connectTimeoutMS=3000&socketTimeoutMS=3500&serverSelectionTimeoutMS=2000"
MONGODB_DB_NAME="xxx"
REDIS_URL="redis://:foobared@localhost:6379/0"
CACHE_MAX_CONNS=4096
CACHE_CONN_TIMEOUT=3.0
CACHE_TIMEOUT=3.5
CACHE_PREFIX="python-cookbook"
MQTT_TOPIC_PREFIX="python-cookbook"
```

### `settings`

```python
"""Settings."""

from functools import lru_cache

from pydantic import MongoDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='allow'
    )

    app_name: str
    app_version: str = '0.1.0'
    app_doc_url: str = '/docs'
    app_description: str = ''
    debug: bool = False

    # MongoDB
    mongodb_url: MongoDsn
    mongodb_db_name: str

    # Cache: Redis
    redis_url: RedisDsn
    cache_max_conns: int = 4096
    cache_conn_timeout: float | None = 3.0
    cache_timeout: float | None = 3.5
    cache_prefix: str

    # MQTT
    mqtt_host: str = "localhost"
    mqtt_port: int = 1883
    mqtt_username: str | None = None
    mqtt_password: str | None = None
    mqtt_timeout: float | None = 3.5
    mqtt_qos: int = 2
    mqtt_topic_prefix: str


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]
```

### App

```python
"""FastAPI App."""

import asyncio
import json
import logging
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TypedDict

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

MONGODB_CLIENT = AsyncIOMotorClient(str(settings.mongodb_url))
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
async def lifespan(_: FastAPI) -> AsyncGenerator:

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

        yield {'redis_client': redis_client, 'mqtt_client': mqtt_client}

        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

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
    cache_val = await request.state.redis_client.get(
        f'{settings.cache_prefix}:examples'
    )
    await request.state.mqtt_client.publish(
        f'{settings.mqtt_topic_prefix}/example',
        payload=json.dumps({'msg': 'hello'}, ensure_ascii=False),
        qos=settings.mqtt_qos,
    )
    return {'db': db_doc, 'cache': cache_val}


app.include_router(router, prefix='/api/router', tags=['router'])
```

### Run

```bash
pipenv run uvicorn --host 0.0.0.0 --port 8000 \
    --proxy-headers \
    --forwarded-allow-ips "*" \
    --workers 8 \
    --limit-concurrency 1024 \
    --backlog 4096 \
    --log-level debug \
    --timeout-keep-alive 5 \
    --use-colors \
    --no-server-header \
    examples.web.fastapi.main:app \
    --log-config examples/web/uvicorn_logging.json
```

## More

- [Quick Start with **`FastAPI`**](fastapi_quickstart)
- [MongoDB **`motor`** - Python Cookbook](../../system_services/mongodb_motor)
- [Redis **`redis`** - Python Cookbook](../../system_services/redis)
- [MQTT **`aiomqtt`** - Python Cookbook](../../system_services/mqtt_aiomqtt)
- [Data Model: **`Pydantic`**](../pydantic)

## References

- [**`FastAPI`**](https://fastapi.tiangolo.com/)
- [Getting Started with MongoDB and FastAPI](https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/)
- [**`Beanie`** - Async Python ODM for MongoDB, based on `Pydantic`](https://beanie-odm.dev/)
- [`PyODMongo`: Async ODM (based on `Pydantic V2`)](https://pyodmongo.dev/)
- [*`Pydantic`*: data part](https://pydantic-docs.helpmanual.io/)
