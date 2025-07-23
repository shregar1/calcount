from fastapi import Request, Response
from fastapi.responses import JSONResponse
from http import HTTPStatus
from starlette.middleware.base import BaseHTTPMiddleware

from constants.api_status import APIStatus

from dtos.responses.base import BaseResponseDTO

from repositories.user import UserRepository

from start_utils import db_session, logger, unprotected_routes, callback_routes

from utilities.jwt import JWTUtility


class AuthenticationMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        logger.debug("Inside authentication middleware")

        urn: str = request.state.urn
        endpoint: str = request.url.path

        if request.method == "OPTIONS":
            return await call_next(request)

        logger.debug(f"Received request for endpoint: {endpoint}")

        if endpoint in unprotected_routes.union(callback_routes):

            logger.debug("Accessing Unprotected Route", urn=request.state.urn)
            response: Response = await call_next(request)
            return response

        logger.debug("Accessing Protected Route", urn=request.state.urn)
        token: str = request.headers.get("authorization")
        if not token or "bearer" not in token.lower():

            logger.debug("Preparing response metadata", urn=request.state.urn)
            response_dto: BaseResponseDTO = BaseResponseDTO(
                transactionUrn=urn,
                status=APIStatus.FAILED,
                responseMessage="JWT Authentication failed.",
                responseKey="error_authetication_error",
                data={},
            )
            http_status_code = HTTPStatus.UNAUTHORIZED
            logger.debug("Prepared response metadata", urn=request.state.urn)
            return JSONResponse(
                content=response_dto.to_dict(), status_code=http_status_code
            )

        try:

            logger.debug(
                "Decoding the authetication token", urn=request.state.urn
            )
            token = token.split(" ")[1]

            user_data: dict = JWTUtility(urn=urn).decode_token(token=token)
            logger.debug(
                "Decoded the authetication token", urn=request.state.urn
            )

            logger.debug(
                "Fetching user logged in status.", urn=request.state.urn
            )
            user = UserRepository(
                urn=urn, session=db_session
            ).retrieve_record_by_id_and_is_logged_in(
                id=user_data.get("user_id"),
                is_logged_in=True,
                is_deleted=False,
            )
            logger.debug(
                "Fetched user logged in status.", urn=request.state.urn
            )

            if not user:

                logger.debug(
                    "Preparing response metadata", urn=request.state.urn
                )
                response_dto: BaseResponseDTO = BaseResponseDTO(
                    transactionUrn=urn,
                    status=APIStatus.FAILED,
                    responseMessage="User Session Expired.",
                    responseKey="error_session_expiry",
                )
                http_status_code = HTTPStatus.UNAUTHORIZED
                logger.debug(
                    "Prepared response metadata", urn=request.state.urn
                )
                return JSONResponse(
                    content=response_dto.to_dict(),
                    status_code=http_status_code,
                )

            request.state.user_id = user_data.get("user_id")
            request.state.user_urn = user_data.get("user_urn")

        except Exception as err:

            logger.debug(
                f"{err.__class__} occured while authentiacting jwt token, {err}",
                urn=request.state.urn,
            )

            logger.debug("Preparing response metadata", urn=request.state.urn)
            response_dto: BaseResponseDTO = BaseResponseDTO(
                transactionUrn=urn,
                status=APIStatus.FAILED,
                responseMessage="JWT Authentication failed.",
                responseKey="error_authetication_error",
            )
            http_status_code = HTTPStatus.UNAUTHORIZED
            logger.debug("Prepared response metadata", urn=request.state.urn)
            return JSONResponse(
                content=response_dto.to_dict(), status_code=http_status_code
            )

        logger.debug(
            "Procceding with the request execution.", urn=request.state.urn
        )
        response: Response = await call_next(request)

        return response
