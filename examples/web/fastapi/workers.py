"""FastAPI workers."""

import logging


async def handle_bytes(message: bytes) -> None:
    logging.warning(message.decode('utf-8'))
