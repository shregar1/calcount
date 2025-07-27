import ulid

from datetime import datetime
from http import HTTPMethod, HTTPStatus

from constants.api_status import APIStatus

from dtos.requests.apis.v1.meal.add import AddMealRequestDTO
from dtos.responses.base import BaseResponseDTO

from errors.unexpected_response_error import UnexpectedResponseError
from models.meal_log import MealLog

from repositories.meal_log import MealLogRepository

from services.apis.v1.meal.abstraction import IMealAPIService

from start_utils import USDA_API_KEY, usda_configuration


class AddMealService(IMealAPIService):

    def __init__(
        self,
        urn: str = None,
        user_urn: str = None,
        api_name: str = None,
        user_id: int = None,
        meal_log_repository: MealLogRepository = None
    ) -> None:
        super().__init__(urn, user_urn, api_name)
        self._urn = urn
        self._user_urn = user_urn
        self._api_name = api_name
        self._user_id = user_id
        self._meal_log_repository = meal_log_repository

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
    def meal_log_repository(self):
        return self._meal_log_repository

    @meal_log_repository.setter
    def meal_log_repository(self, value):
        self._meal_log_repository = value

    async def run(self, request_dto: AddMealRequestDTO) -> BaseResponseDTO:

        self.logger.info("Fetching meal details")
        url = usda_configuration.url.format(
                query=request_dto.meal_name,
                api_key=USDA_API_KEY
            )
        meal_details: dict = await self.make_api_request(
            url=url,
            method=HTTPMethod.GET,
            headers={"x-api-key": USDA_API_KEY},
            payload=request_dto.model_dump()
        )
        self.logger.info("Meal details fetched")

        self.logger.info("Parsing meal details")
        meal_data: dict = await self.process_meal_details(
            meal_name=request_dto.meal_name,
            servings=request_dto.servings,
            meal_details=meal_details,
            get_instructions=request_dto.get_instructions
        )
        self.logger.info("Meal details parsed")

        total_calories_per_serving = meal_data.get("total_calories")
        calories_unit = meal_data.get("calories_unit")
        total_calories = total_calories_per_serving * request_dto.servings

        if total_calories_per_serving < 0:
            self.logger.error("Calories cannot be negative")
            raise UnexpectedResponseError(
                responseMessage="Calories cannot be negative.",
                responseKey="error_negative_calories",
                httpStatusCode=HTTPStatus.UNPROCESSABLE_ENTITY,
            )

        self.logger.info("Adding meal")
        meal_log: MealLog = MealLog(
            urn=ulid.ulid(),
            user_id=self.user_id,
            meal_name=request_dto.meal_name,
            servings=request_dto.servings,
            nutrients=meal_data.get("nutrients"),
            ingredients=meal_data.get("ingredients"),
            instructions=meal_data.get("instructions"),
            total_calories_per_serving=total_calories_per_serving,
            calories_unit=calories_unit,
            total_calories=total_calories,
            created_on=datetime.now(),
            created_by=self.user_id
        )
        meal_log: MealLog = self.meal_log_repository.create_record(
            record=meal_log
        )
        self.logger.info("Meal added")

        return BaseResponseDTO(
            transactionUrn=self.urn,
            status=APIStatus.SUCCESS,
            responseMessage="Successfully added the meal.",
            responseKey="success_add_meal",
            data={
                "urn": meal_log.urn,
                "meal_name": meal_log.meal_name,
                "servings": meal_log.servings,
                "nutrients_per_serving": meal_log.nutrients,
                "ingredients_per_serving": meal_log.ingredients,
                "instructions_per_serving": meal_log.instructions,
                "total_calories_per_serving":
                    meal_log.total_calories_per_serving,
                "total_calories": meal_log.total_calories,
                "calories_unit": meal_log.calories_unit,
                "created_on": str(meal_log.created_on),
                "source": "usda"
            },
        )
