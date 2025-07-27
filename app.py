import os
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from http import HTTPStatus
from loguru import logger

from controllers.user import router as UserRouter
from controllers.apis import router as APISRouter

from middlewares.authetication import AuthenticationMiddleware
from middlewares.rate_limit import (
    RateLimitMiddleware, RateLimitConfig
)
from middlewares.security_headers import (
    SecurityHeadersMiddleware,
    SecurityHeadersConfigDTO
)
from middlewares.request_context import RequestContextMiddleware


app = FastAPI()

load_dotenv()
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"error: {exc.errors()}")
    for error in exc.errors():
        if "ctx" in error:
            error.pop("ctx")
    response_payload: dict = {
        "transactionUrn": request.state.urn,
        "responseMessage": "Bad or missing input.",
        "responseKey": "error_bad_input",
        "errors": exc.errors(),
    }
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content=response_payload,
    )


@app.get("/health")
async def health_check():
    return {"status": "ok"}


app.add_middleware(middleware_class=TrustedHostMiddleware, allowed_hosts=["*"])
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

logger.info("Initialising middleware stack")
security_config = SecurityHeadersConfigDTO(
    enable_hsts=True,
    enable_csp=True,
    hsts_max_age=31536000,
    hsts_include_subdomains=True
)
app.add_middleware(SecurityHeadersMiddleware, **security_config.__dict__)
rate_limit_config = RateLimitConfig(
    requests_per_minute=60,
    requests_per_hour=1000,
    burst_limit=10,
    enable_sliding_window=True,
    enable_token_bucket=False
)
app.add_middleware(RateLimitMiddleware, config=rate_limit_config)
app.add_middleware(AuthenticationMiddleware)
app.add_middleware(RequestContextMiddleware)
logger.info("Initialised middleware stack")

logger.info("Initialising routers")
# USER ROUTER
app.include_router(UserRouter)
# APIS ROUTER
app.include_router(APISRouter)
logger.info("Initialised routers")

if __name__ == "__main__":
    uvicorn.run("app:app", host=HOST, port=PORT, reload=True)
