from http import HTTPMethod

from constants.api_status import APIStatus

from dtos.requests.apis.v1.meal.fetch import FetchMealRequestDTO
from dtos.responses.base import BaseResponseDTO

from repositories.meal_log import MealLogRepository

from services.apis.v1.meal.abstraction import IMealAPIService

from start_utils import USDA_API_KEY, usda_configuration


class FetchMealService(IMealAPIService):

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

    async def run(self, request_dto: FetchMealRequestDTO) -> BaseResponseDTO:

        self.logger.info("Fetching meal details")
        url = usda_configuration.url.format(
                query=request_dto.meal_name,
                api_key=USDA_API_KEY
            )
        meal_details = self.make_api_request(
            url=url,
            method=HTTPMethod.GET,
            headers={"x-api-key": USDA_API_KEY},
            payload=request_dto.model_dump()
        )
        self.logger.info("Meal details fetched")

        self.logger.info("Parsing meal details")
        meal_data = self.process_meal_details(
            meal_name=request_dto.meal_name,
            servings=request_dto.servings,
            meal_details=meal_details,
            get_instructions=request_dto.get_instructions
        )
        self.logger.info("Meal details parsed")

        total_calories_per_serving = meal_data.get("total_calories")
        calories_unit = meal_data.get("calories_unit")
        total_calories = total_calories_per_serving * request_dto.servings

        return BaseResponseDTO(
            transactionUrn=self.urn,
            status=APIStatus.SUCCESS,
            responseMessage="Successfully fetched the meal details.",
            responseKey="success_fetch_meal",
            data={
                "meal_name": request_dto.meal_name,
                "servings": request_dto.servings,
                "nutrients_per_serving": meal_data.get("nutrients"),
                "ingredients_per_serving": meal_data.get("ingredients"),
                "instructions_per_serving": meal_data.get("instructions"),
                "total_calories_per_serving": total_calories_per_serving,
                "total_calories": total_calories,
                "calories_unit": calories_unit,
                "source": "usda"
            },
        )
