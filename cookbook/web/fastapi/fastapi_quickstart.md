# Quick Start with `FastAPI`

## Installation

```bash
uv init --python 3.12

uv add fastapi[all] uvicorn[standard]
uv add --dev ruff mypy

# JWT
uv add python-jose[cryptography] types-python-jose

# HTTP Request
uv add aiohttp
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
requires-python = "~=3.12"
license-files = ["LICEN[CS]E*", "vendored/licenses/*.txt", "AUTHORS.md"]
maintainers = [
    {name = "<Maintainer Name>", email = "<maintainer@email>"},
]
keywords = ["xxx"]
classifiers = [
    "Development Status :: 2 - Pre-Alpha",

    "Intended Audience :: Developers",
    "Topic :: Software Development :: Documentation",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",

    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: Implementation :: CPython",
    "Operating System :: OS Independent",
    "Typing :: Typed",
]
dependencies = [
    "fastapi[all]",
    "uvicorn[standard]",

    "python-jose[cryptography]",
    "types-python-jose",

    #"aiohttp",
]
dynamic = ["version"]

[project.urls]
Home = "<URL>"
Documentation = "<URL>"
Repository = "<URL>"

[tool.setuptools]
py-modules = ['app', 'src']

[[tool.uv.index]]
url = "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"
default = true

[dependency-groups]
dev = [
    "ruff>=0.11.8",
    "mypy>=1.15.0",
]

[tool.ruff]
line-length = 100
lint.extend-safe-fixes = [
    # non-pep585-annotation
    "UP006",
]
lint.select = [
    # flake8-bugbear
    "B",
    # flake8-comprehensions
    "C4",
    # pycodestyle
    "E",
    # Pyflakes errors
    "F",
    # isort
    "I",
    # flake8-simplify
    "SIM",
    # flake8-tidy-imports
    "TID",
    # pyupgrade
    "UP",
    # Pyflakes warnings
    "W",
]
lint.ignore = []

[tool.ruff.format]
quote-style = "single"

[tool.mypy]
python_version = "3.12"
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

[tool.pyright]
include = [
    "src",
    "app",
]
exclude = [
    ".git",
    "**/__pycache__",
    ".venv",
    "**/*.egg-info",
    ".ruff_cache",
    ".mypy_cache",
    ".pytest_cache",
    ".tox",
]
reportGeneralTypeIssues = "none"
reportUnboundVariable = "none"
stubPath = ""
pythonVersion = "3.12"
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

### `settings_simple.py`

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
"""FastAPI Simple App."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI

from examples.web.fastapi.settings_simple import get_settings

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
    uvicorn.run(app='main_simple:app', host='', reload=True)
```

## Run

See [Uvicorn: ASGI, WebSockets - Python Cookbook](../uvicorn).

## More

- [Python Project - Python Cookbook](../../build/project)
- [ASGI Web Server: **`Uvicorn`** - Python Cookbook](../uvicorn)
- [Data Model: **`Pydantic`** - Python Cookbook](../pydantic)
- [FastAPI App - Python Cookbook](fastapi_app)

## References

- [**`FastAPI`**](https://fastapi.tiangolo.com/)
- [*`Starlette`*: *ASGI* Web part](https://www.starlette.io/)
- [*`Pydantic`*: data part](https://pydantic-docs.helpmanual.io/)
- [*`Swagger`*: *OpenAPI*](https://swagger.io/)
- [Awesome List for FastAPI](https://github.com/mjhea0/awesome-fastapi)
