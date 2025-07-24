from fastapi import Request, Depends
from fastapi.responses import JSONResponse
from http import HTTPStatus
from sqlalchemy.orm import Session
from typing import Callable

from abstractions.controller import IController

from constants.api_lk import APILK
from constants.api_status import APIStatus

from dependencies.apis.v1.meal.add import AddMealDependency
from dependencies.db import DBDependency

from dtos.requests.apis.v1.meal.add import AddMealRequestDTO
from dtos.responses.base import BaseResponseDTO

from errors.bad_input_error import BadInputError
from errors.not_found_error import NotFoundError
from errors.unexpected_response_error import UnexpectedResponseError

from utilities.dictionary import DictionaryUtility


class AddMealController(IController):

    def __init__(self, urn: str = None) -> None:
        super().__init__(urn)
        self.api_name = APILK.ADD_MEAL

    async def post(
        self,
        request: Request,
        request_payload: AddMealRequestDTO,
        session: Session = Depends(DBDependency.derive),
        add_meal_service_factory: Callable = Depends(AddMealDependency.derive)
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
            service = add_meal_service_factory(
                urn=self.urn,
                user_urn=self.user_urn,
                api_name=self.api_name,
                user_id=self.user_id,
                session=session,
            )
            response_dto: BaseResponseDTO = await service.run(
                request_dto=request_payload
            )

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
