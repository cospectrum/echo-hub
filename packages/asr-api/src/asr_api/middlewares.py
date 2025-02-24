import uuid
from typing import Awaitable, Callable
from fastapi import Request, Response

from . import ctx


Next = Callable[[Request], Awaitable[Response]]

TRACE_ID_HEADER = "X-Trace-Id"


async def add_trace_id(request: Request, call_next: Next) -> Response:
    trace_id = request.headers.get(TRACE_ID_HEADER, uuid.uuid4().hex)
    ctx.trace_id.set(trace_id)
    response = await call_next(request)
    response.headers[TRACE_ID_HEADER] = trace_id
    return response
