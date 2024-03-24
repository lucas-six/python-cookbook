"""FastAPI routers."""

from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class BasicResponse(BaseModel):
    code: int = 0
    message: str = 'ok'
    item_id: str | None = None


@router.get(
    '/hello/',
    response_model=BasicResponse,
    summary='API Summary',
)
async def hello() -> BasicResponse:
    return BasicResponse()


class User(BaseModel):
    id: int
    name: str = 'Lucas'
    signup_time: datetime | None = None
    friends: list[str] = []


@router.get('/model')
async def model() -> dict[str, str | list[str | datetime | None]]:
    user_data: dict[str, str | list[str | datetime | None]] = {
        'id': '123',
        'signup_time': '2019-06-01 12:22',
        'friends': [],
    }

    return user_data
