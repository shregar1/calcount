from fastapi import Request, Depends
from fastapi.responses import JSONResponse
from http import HTTPStatus
from loguru import logger
from sqlalchemy.orm import Session
from typing import Callable

from abstractions.controller import IController

from constants.api_lk import APILK
from constants.api_status import APIStatus

from dependencies.db import DBDependency
from dependencies.repositiories.meal_log import MealLogRepositoryDependency
from dependencies.services.apis.v1.meal.fetch import FetchMealServiceDependency
from dependencies.utilities.dictionary import DictionaryUtilityDependency

from dtos.requests.apis.v1.meal.fetch import FetchMealRequestDTO
from dtos.responses.base import BaseResponseDTO

from errors.bad_input_error import BadInputError
from errors.not_found_error import NotFoundError
from errors.unexpected_response_error import UnexpectedResponseError

from repositories.meal_log import MealLogRepository
from utilities.dictionary import DictionaryUtility


class FetchMealController(IController):

    def __init__(
        self,
        urn: str = None,
        user_urn: str = None,
        api_name: str = None,
        user_id: str = None,
    ) -> None:
        super().__init__(urn)
        self._urn: str = urn
        self._user_urn: str = user_urn
        self._api_name: str = APILK.SEARCH_MEAL
        self._user_id: str = user_id
        self._logger: logger = self.logger
        self._dictionary_utility: DictionaryUtility = None

    @property
    def urn(self):
        return self._urn

    @urn.setter
    def urn(self, value):
        self._urn = value

    @property
    def user_urn(self):
        return self._user_urn

    @user_urn.setter
    def user_urn(self, value):
        self._user_urn = value

    @property
    def api_name(self):
        return self._api_name

    @api_name.setter
    def api_name(self, value):
        self._api_name = value

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    @property
    def dictionary_utility(self):
        return self._dictionary_utility

    @dictionary_utility.setter
    def dictionary_utility(self, value):
        self._dictionary_utility = value

    async def get(
        self,
        request: Request,
        request_payload: FetchMealRequestDTO,
        session: Session = Depends(DBDependency.derive),
        meal_log_repository: MealLogRepository = Depends(
            MealLogRepositoryDependency.derive
        ),
        fetch_meal_service_factory: Callable = Depends(
            FetchMealServiceDependency.derive
        ),
        dictionary_utility: DictionaryUtility = Depends(
            DictionaryUtilityDependency.derive
        ),
    ) -> JSONResponse:

        self.logger.debug("Fetching request URN")
        self.urn: str = request.state.urn
        self.user_id: str = getattr(request.state, "user_id", None)
        self.user_urn: str = getattr(request.state, "user_urn", None)
        self.logger: logger = self.logger.bind(
            urn=self.urn,
            user_urn=self.user_urn,
            api_name=self.api_name,
            user_id=self.user_id,
        )
        self.dictionary_utility: DictionaryUtility = (
            dictionary_utility(
                urn=self.urn,
                user_urn=self.user_urn,
                api_name=self.api_name,
                user_id=self.user_id,
            )
        )
        self.meal_log_repository: MealLogRepository = meal_log_repository(
            urn=self.urn,
            user_urn=self.user_urn,
            api_name=self.api_name,
            user_id=self.user_id,
            session=session,
        )
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

            self.logger.debug("Running fetch meal service")
            response_dto: BaseResponseDTO = await fetch_meal_service_factory(
                urn=self.urn,
                user_urn=self.user_urn,
                api_name=self.api_name,
                user_id=self.user_id,
                meal_log_repository=self.meal_log_repository,
            ).run(
                request_dto=request_payload
            )

            self.logger.debug("Preparing response metadata")
            http_status_code = HTTPStatus.OK
            self.logger.debug("Prepared response metadata")

        except (BadInputError, UnexpectedResponseError, NotFoundError) as err:

            self.logger.error(
                f"{err.__class__} error occured while fetching meal: {err}"
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
                f"{err.__class__} error occured while fetching meal: {err}"
            )

            self.logger.debug("Preparing response metadata")
            response_dto: BaseResponseDTO = BaseResponseDTO(
                transactionUrn=self.urn,
                status=APIStatus.FAILED,
                responseMessage="Failed to fetch meal.",
                responseKey="error_internal_server_error",
                data={},
            )
            http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            self.logger.debug("Prepared response metadata")

        return JSONResponse(
            content=self.dictionary_utility.convert_dict_keys_to_camel_case(
                response_dto.to_dict()
            ),
            status_code=http_status_code,
        )
