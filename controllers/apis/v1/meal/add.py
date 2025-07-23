from fastapi import Request
from fastapi.responses import JSONResponse
from http import HTTPStatus

from abstractions.controller import IController

from constants.api_lk import APILK
from constants.api_status import APIStatus

from dtos.requests.api.meal.add import AddMealRequestDTO

from dtos.responses.base import BaseResponseDTO

from errors.bad_input_error import BadInputError
from errors.not_found_error import NotFoundError
from errors.unexpected_response_error import UnexpectedResponseError

from repositories.user import UserRepository

from services.apis.meal.add import AddMealService

from start_utils import db_session

from utilities.dictionary import DictionaryUtility


class AddMealController(IController):

    def __init__(self, urn: str = None) -> None:
        super().__init__(urn)
        self.api_name = APILK.LOGIN

    async def post(
        self,
        request: Request,
        request_payload: AddMealRequestDTO
    ) -> JSONResponse:

        self.logger.debug("Fetching request URN")
        self.urn = request.state.urn
        self.user_id = getattr(request.state, "user_id", None)
        self.user_urn = getattr(request.state, "user_urn", None)
        self.logger = self.logger.bind(
            urn=self.urn, user_urn=self.user_urn, api_name=self.api_name
        )
        self.dictionary_utility = DictionaryUtility(urn=self.urn)

        try:

            self.logger.debug("Validating request")
            await self.validate_request(
                urn=self.urn,
                user_urn=self.user_urn,
                request_payload=request_payload.model_dump(),
                request_headers=dict(request.headers.mutablecopy()),
                api_name=self.api_name,
                user_id=self.user_id,
            )
            self.logger.debug("Verified request")

            self.logger.debug("Running login user service")
            response_dto: BaseResponseDTO = await AddMealService(
                urn=self.urn,
                user_urn=self.user_urn,
                api_name=self.api_name,
                user_id=self.user_id,
                user_repository=UserRepository(
                    urn=self.urn,
                    user_urn=self.user_urn,
                    api_name=self.api_name,
                    session=db_session,
                ),
            ).run(request_dto=request_payload)

            self.logger.debug("Preparing response metadata")
            http_status_code = HTTPStatus.OK
            self.logger.debug("Prepared response metadata")

        except (BadInputError, UnexpectedResponseError, NotFoundError) as err:

            self.logger.error(
                f"{err.__class__} error occured while adding meal: {err}"
            )
            self.logger.debug("Preparing response metadata")
            response_dto: BaseResponseDTO = BaseResponseDTO(
                transactionUrn=self.urn,
                status=APIStatus.FAILED,
                responseMessage=err.responseMessage,
                responseKey=err.responseKey,
                data={},
            )
            http_status_code = err.http_status_code
            self.logger.debug("Prepared response metadata")

        except Exception as err:

            self.logger.error(
                f"{err.__class__} error occured while adding meal: {err}"
            )

            self.logger.debug("Preparing response metadata")
            response_dto: BaseResponseDTO = BaseResponseDTO(
                transactionUrn=self.urn,
                status=APIStatus.FAILED,
                responseMessage="Failed to add meal.",
                responseKey="error_internal_server_error",
                data={},
            )
            http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            self.logger.debug("Prepared response metadata")

        return JSONResponse(
            content=response_dto.to_dict(), status_code=http_status_code
        )
