# Quick Start with `FastAPI`

## Installation

```bash
pipenv --python 3.11

pipenv install pydantic
pipenv install fastapi[all]
pipenv install uvicorn[standard]

pipenv install --dev black isort mypy pylint
pipenv install --dev pylint-pydantic

# JWT
pipenv install python-jose[cryptography]
pipenv install types-python-jose

# HTTP Request
pipenv install aiohttp

# MQTT
pipenv install aiomqtt
```

## `pyproject.toml`

```ini
[project]
name = "<project_name>"
description = "<project description>"
authors = [
    {name = "<Author Name>", email = "<author@email>"},
    {name = "Lucas", email = "lucassix.lee@gmail.com"},
]
readme = "README.md"
requires-python = "~=3.11"
license = {file = "LICENSE"}
maintainers = [
    {name = "<Maintainer Name>", email = "<maintainer@email>"},
]
keywords = ["xxx"]
classifiers = [
    "Development Status :: 1 - Planning",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "License :: OSI Approved :: Apache Software License",
    "Typing :: Typed",
]
dependencies = [
    "pydantic",
    "fastapi[all]",
    "uvicorn[standard]",

    "python-jose[cryptography]",
    "types-python-jose",

    #"aiohttp",
    #"aio-mqtt",
]
dynamic = ["version"]

[project.optional-dependencies]
test = [
    "black",
    "isort",
    "mymy",
    "pylint",
    "pylint-pydantic",
]
doc = []

[project.urls]
Home = "<URL>"
Documentation = "<URL>"
Source = "<URL>"

[tool.black]
line-length = 88
target-version = ['py310', 'py311']
skip-string-normalization = true
include = '\.pyi?$'
extend-exclude = '''
tests/.*\.py$
migrations/.*\.py$
'''

[tool.isort]
src_paths = ["src", "app"]
atomic = true
profile = "black"
# skip = [
#    '.bzr',
#    '.direnv',
#    '.eggs',
#    '.git',
#    '.hg',
#    '.mypy_cache',
#    '.nox',
#    '.pants.d',
#    '.svn',
#    '.tox',
#    '.venv',
#    '__pypackages__',
#    '_build',
#    'buck-out',
#    'build',
#    'dist',
#    'node_modules',
#    'venv'
# ]
skip_gitignore = true
extend_skip = [".gitignore", ".env", ".dockerignore"]
# skip_glob = []
extend_skip_glob = []

[tool.mypy]
python_version = "3.11"
plugins = [
    "pydantic.mypy"
]
exclude = [
]
follow_imports = "silent"
warn_redundant_casts = true
warn_unused_ignores = true
warn_unused_configs = true
disallow_any_generics = false
check_untyped_defs = true
no_implicit_reexport = true
disallow_untyped_defs = true

[tool.pydantic-mypy]
init_forbid_extra = true
init_typed = true
warn_required_dynamic_aliases = true
warn_untyped_fields = true

[tool.pylint.main]
recursive = true
py-version = 3.11
jobs = 0
ignore = "CVS,.git,__pycache__,.mypy_cache,tests"
ignore-paths = "tests"
ignore-patterns = "test_.*.py"
ignored-classes = "Body"
extension-pkg-whitelist = "pydantic"
load-plugins = [
    "pylint.extensions.bad_builtin",
    "pylint_pydantic",
]

[tool.pylint.'FORMAT']
max-line-length = 88

[tool.pylint.'LOGGING']
logging-format-style = "new"

[tool.pylint.'MESSAGES CONTROL']
disable = [
    "raw-checker-failed",
    "bad-inline-option",
    "locally-disabled",
    "file-ignored",
    "suppressed-message",
    "deprecated-pragma",
    "use-symbolic-message-instead",
    "logging-fstring-interpolation",
    "missing-function-docstring",
    "missing-class-docstring",
]
enable = [
    "c-extension-no-member",
    "useless-suppression",
]

[tool.pylint.design]
max-args = 15
min-public-methods = 0
max-locals = 25

[tool.pylint.deprecated_builtins]
bad-functions = ["map", "filter", "print"]

[tool.pyright]
include = [
    "src",
    "app",
]
exclude = [
    ".git",
    "**/__pycache__",
    "**/.mypy_cache",
]
reportGeneralTypeIssues = "none"
reportUnboundVariable = "none"
stubPath = ""
pythonVersion = "3.11"
```

## App

### `.env`

```ini
# .env

APP_NAME="FastAPI App"
APP_VERSION="v1.0.0"
APP_DESCRIPTION="FastAPI app description."
DEBUG=true
```

### `settings`

```python
"""Settings."""

from functools import lru_cache

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


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]
```

### App

```python
"""FastAPI App."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI

from examples.web.fastapi.settings import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[Any, Any]:
    yield


app: FastAPI = FastAPI(
    title=settings.app_name,
    docs_url=settings.app_doc_url,
    debug=settings.debug,
    openapi_url=f'{settings.app_doc_url}/openapi.json',
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)


@app.get('/api')
async def root() -> dict[str, str]:
    return {'Hello': 'World'}


# Only for develop environment
if __name__ == '__main__':
    uvicorn.run(app='main:app', host='', reload=True)
```

### Custom OpenAPI static files

```python
"""FastAPI OpenAPI (v3.1) with custom static files."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from examples.web.fastapi.routers import router
from examples.web.fastapi.settings import get_settings

settings = get_settings()
API_DOC_STATIC_DIR = 'examples/web/fastapi/static'
API_DOC_STATIC_PATH = f'{settings.app_doc_url}/{API_DOC_STATIC_DIR}'


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[Any, Any]:
    yield


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
        title=app.title + " - Swagger UI",
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
        title=app.title + " - ReDoc",
        redoc_js_url=f'{API_DOC_STATIC_PATH}/redoc.standalone.js',
    )


@app.get('/api')
async def root() -> dict[str, str]:
    return {'Hello': 'World'}


app.include_router(router, prefix='/api/router', tags=['router'])


# Only for develop environment
if __name__ == '__main__':
    uvicorn.run(app='main:app', host='', reload=True)
```

## Run

See [Uvicorn: ASGI, WebSockets - Python Cookbook](../uvicorn).

## More

- [Python Project - Python Cookbook](../../build/project)
- [ASGI Web Server: **`Uvicorn`** - Python Cookbook](../uvicorn)
- [Data Model: **`Pydantic`** - Python Cookbook](../pydantic)
- [with MongoDB: **`motor`** - Python Cookbook](fastapi_mongodb)
- [with Redis: **`redis`** - Python Cookbook](../../system_services/redis)

## References

- [**`FastAPI`**](https://fastapi.tiangolo.com/)
- [*`Starlette`*: *ASGI* Web part](https://www.starlette.io/)
- [*`Pydantic`*: data part](https://pydantic-docs.helpmanual.io/)
- [*`Swagger`*: *OpenAPI*](https://swagger.io/)
- [Awesome List for FastAPI](https://github.com/mjhea0/awesome-fastapi)
