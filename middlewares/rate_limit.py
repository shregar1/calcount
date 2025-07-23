from fastapi import Request
from http import HTTPStatus
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from time import time

from start_utils import logger


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
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
