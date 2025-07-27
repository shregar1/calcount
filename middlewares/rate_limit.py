import time
import asyncio
from typing import Dict, Optional, Tuple
from collections import defaultdict, deque
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from http import HTTPStatus

from constants.api_status import APIStatus
from constants.default import Default
from dtos.responses.base import BaseResponseDTO
from start_utils import logger


class RateLimitConfig:
    """Configuration for rate limiting."""

    def __init__(
        self,
        requests_per_minute: int = Default.RATE_LIMIT_REQUESTS_PER_MINUTE,
        requests_per_hour: int = Default.RATE_LIMIT_REQUESTS_PER_HOUR,
        burst_limit: int = Default.RATE_LIMIT_BURST_LIMIT,
        window_size: int = Default.RATE_LIMIT_WINDOW_SECONDS,
        enable_sliding_window: bool = True,
        enable_token_bucket: bool = False,
        enable_fixed_window: bool = False,
    ):
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.burst_limit = burst_limit
        self.window_size = window_size
        self.enable_sliding_window = enable_sliding_window
        self.enable_token_bucket = enable_token_bucket
        self.enable_fixed_window = enable_fixed_window


class RateLimitStore:
    """In-memory store for rate limiting data."""

    def __init__(self):
        self._sliding_windows: Dict[str, deque] = defaultdict(deque)
        self._lock = asyncio.Lock()

    async def check_sliding_window(
        self, key: str, limit: int, window: int
    ) -> Tuple[bool, int]:
        """Check sliding window rate limit."""
        async with self._lock:
            now = time.time()
            window_start = now - window

            while (
                self._sliding_windows[key] and
                self._sliding_windows[key][0] < window_start
            ):
                self._sliding_windows[key].popleft()

            if len(self._sliding_windows[key]) >= limit:
                return False, len(self._sliding_windows[key])

            self._sliding_windows[key].append(now)
            return True, len(self._sliding_windows[key])

    async def cleanup_old_entries(self, max_age: int = 3600):
        """Clean up old rate limiting entries."""
        async with self._lock:
            now = time.time()

            for key in list(self._sliding_windows.keys()):
                while (
                    self._sliding_windows[key] and
                    self._sliding_windows[key][0] < now - max_age
                ):
                    self._sliding_windows[key].popleft()

                if not self._sliding_windows[key]:
                    del self._sliding_windows[key]


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware with multiple strategies."""

    def __init__(
        self,
        app,
        config: Optional[RateLimitConfig] = None,
        excluded_paths: Optional[set] = None,
        excluded_methods: Optional[set] = None,
    ):
        super().__init__(app)
        self.config = config or RateLimitConfig()
        self.excluded_paths = (
            excluded_paths or {"/health", "/docs", "/openapi.json"}
        )
        self.excluded_methods = excluded_methods or {"OPTIONS"}
        self.store = RateLimitStore()
        asyncio.create_task(self._cleanup_task())

    async def _cleanup_task(self):
        """Periodic cleanup of old rate limiting entries."""
        while True:
            await asyncio.sleep(300)
            await self.store.cleanup_old_entries()

    def _get_client_identifier(self, request: Request) -> str:
        """Get unique identifier for the client."""
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        return request.client.host if request.client else "unknown"

    def _get_rate_limit_key(self, request: Request) -> str:
        """Generate rate limit key based on client and endpoint."""
        client_id = self._get_client_identifier(request)
        endpoint = request.url.path
        method = request.method

        return f"{client_id}:{method}:{endpoint}"

    async def _check_rate_limits(
        self,
        key: str,
    ) -> Tuple[bool, Dict[str, any]]:
        """Check all enabled rate limiting strategies."""
        results = {}

        if self.config.enable_sliding_window:
            allowed, count = await self.store.check_sliding_window(
                f"{key}:sliding:minute",
                self.config.requests_per_minute,
                60
            )
            results["sliding_minute"] = {"allowed": allowed, "count": count}
            if not allowed:
                return False, results

        if self.config.enable_sliding_window:
            allowed, count = await self.store.check_sliding_window(
                f"{key}:sliding:hour",
                self.config.requests_per_hour,
                3600
            )
            results["sliding_hour"] = {"allowed": allowed, "count": count}
            if not allowed:
                return False, results

        return True, results

    async def dispatch(self, request: Request, call_next):
        """Process the request with rate limiting."""

        if (
            request.url.path in self.excluded_paths or
            request.method in self.excluded_methods
        ):
            return await call_next(request)

        key = self._get_rate_limit_key(request)

        allowed, results = await self._check_rate_limits(key)

        if not allowed:
            exceeded_limits = []
            for strategy, result in results.items():
                if not result.get("allowed", True):
                    exceeded_limits.append(strategy)

            response_dto = BaseResponseDTO(
                transactionUrn=request.state.urn,
                status=APIStatus.FAILED,
                responseMessage="Rate limit exceeded. Please try again later.",
                responseKey="error_rate_limit_exceeded",
                data={
                    "exceeded_limits": exceeded_limits,
                    "retry_after": 60,  # seconds
                }
            )

            logger.warning(
                f"Rate limit exceeded for {key}",
                urn=request.state.urn,
                client_ip=self._get_client_identifier(request),
                exceeded_limits=exceeded_limits
            )

            return JSONResponse(
                content=response_dto.model_dump(),
                status_code=HTTPStatus.TOO_MANY_REQUESTS,
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(self.config.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time()) + 60)
                }
            )

        response = await call_next(request)

        remaining = max(0, self.config.requests_per_minute - 1)
        reset_time = int(time.time()) + 60

        response.headers["X-RateLimit-Limit"] = str(
            self.config.requests_per_minute
        )
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(reset_time)

        return response
