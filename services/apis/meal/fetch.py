from http import HTTPMethod

from constants.api_status import APIStatus

from dtos.requests.api.meal.fetch import FetchMealRequestDTO
from dtos.responses.base import BaseResponseDTO

from repositories.meal_log import MealLogRepository

from services.apis.meal.abstraction import IMealAPIService

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
        self.urn = urn
        self.user_urn = user_urn
        self.api_name = api_name
        self.user_id = user_id
        self.meal_log_repository = meal_log_repository

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
                "calories_unit": calories_unit,
                "total_calories": total_calories,
            },
        )
