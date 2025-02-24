import logging
import uuid
from typing import Awaitable, Callable
from fastapi import Request, Response

from . import ctx


logger = logging.getLogger(__name__)

Next = Callable[[Request], Awaitable[Response]]

TRACE_ID_HEADER = "X-Trace-Id"


async def add_trace_id(request: Request, call_next: Next) -> Response:
    trace_id = request.headers.get(TRACE_ID_HEADER, uuid.uuid4().hex)
    ctx.trace_id.set(trace_id)
    response = await call_next(request)
    response.headers[TRACE_ID_HEADER] = trace_id
    return response


async def log_request_info(request: Request, call_next: Next) -> Response:
    logger.info(
        "request info: %s",
        dict(
            request_path=request.url.path,
        ),
    )
    return await call_next(request)
