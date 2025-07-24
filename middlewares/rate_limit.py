from fastapi import Request
from http import HTTPStatus
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from time import time

from start_utils import (
    logger,
    RATE_LIMIT_MAX_REQUESTS,
    RATE_LIMIT_WINDOW_SECONDS,
)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.max_requests = RATE_LIMIT_MAX_REQUESTS
        self.window_seconds = RATE_LIMIT_WINDOW_SECONDS
        self.clients = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time()
        window = int(now // self.window_seconds)

        if client_ip not in self.clients:
            self.clients[client_ip] = {}
            logger.debug(f"New client tracked: {client_ip}")

        if window not in self.clients[client_ip]:
            self.clients[client_ip] = {window: 1}
            logger.debug(f"New window started for {client_ip}: {window}")
        else:
            self.clients[client_ip][window] += 1
            logger.debug(
                f"Request count for {client_ip} in window {window}: "
                f"{self.clients[client_ip][window]}"
            )

        if self.clients[client_ip][window] > self.max_requests:
            logger.warning(
                f"Rate limit exceeded for {client_ip} in window {window}"
            )
            return JSONResponse(
                status_code=HTTPStatus.TOO_MANY_REQUESTS,
                content={"detail": "Rate limit exceeded. Try again later."}
            )

        response = await call_next(request)
        return response
