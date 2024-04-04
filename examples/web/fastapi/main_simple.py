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
