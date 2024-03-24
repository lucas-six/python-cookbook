# `FastAPI` with MongoDB

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
APP_VERSION="v1.0.0"
APP_DESCRIPTION="FastAPI app description."
DEBUG=true
MONGODB_URL="mongodb://localhost:27017/?replicaSet=xxx&maxPoolSize=4096&connectTimeoutMS=3000&socketTimeoutMS=3500&serverSelectionTimeoutMS=2000"
MONGODB_DB_NAME="xxx"
```

### `settings`

```python
"""Settings with MongoDB."""

from functools import lru_cache

from pydantic import MongoDsn
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
    mongodb_url: MongoDsn
    mongodb_db_name: str


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]
```

### App

```python
"""FastAPI with MongoDB."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from motor.core import AgnosticClient
from motor.motor_asyncio import AsyncIOMotorClient

from examples.web.fastapi.routers import router
from examples.web.fastapi.settings_mongodb import get_settings

settings = get_settings()
API_DOC_STATIC_DIR = 'examples/web/fastapi/static'
API_DOC_STATIC_PATH = f'{settings.app_doc_url}/{API_DOC_STATIC_DIR}'

MONGODB_CLIENT: AgnosticClient = AsyncIOMotorClient(str(settings.mongodb_url))
DB_XXX = MONGODB_CLIENT[settings.mongodb_db_name]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    yield
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
async def root() -> dict[str, str]:
    await app.state.mongodb_db['x'].find_one({''})
    return {'Hello': 'World'}


app.include_router(router, prefix='/api/router', tags=['router'])


# Only for develop environment
if __name__ == '__main__':
    uvicorn.run(app='main:app', host='', reload=True)
```

## More

- [Quick Start with **`FastAPI`**](fastapi_quickstart)
- [MongoDB **`motor`** - Python Cookbook](../../system_services/mongodb_motor)
- [Data Model: **`Pydantic`**](../pydantic)

## References

- [**`FastAPI`**](https://fastapi.tiangolo.com/)
- [Getting Started with MongoDB and FastAPI](https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/)
- [**`Beanie`** - Async Python ODM for MongoDB, based on `Pydantic`](https://beanie-odm.dev/)
- [`PyODMongo`: Async ODM (based on `Pydantic V2`)](https://pyodmongo.dev/)
- [*`Pydantic`*: data part](https://pydantic-docs.helpmanual.io/)
