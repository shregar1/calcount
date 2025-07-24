from http import HTTPMethod

from constants.api_status import APIStatus

from dtos.requests.apis.v1.meal.fetch import FetchMealRequestDTO
from dtos.responses.base import BaseResponseDTO

from repositories.meal_log import MealLogRepository

from services.apis.v1.meal.abstraction import IMealAPIService


class FetchMealHistoryService(IMealAPIService):

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

        self.logger.info("Fetching meal history")
        meal_history = self.meal_log_repository.retrieve_history_by_user_id(
            user_id=self.user_id
        )
        self.logger.info("Meal history fetched")

        meal_history_data = []
        for meal in meal_history:
            meal_history_data.append({
                "meal_name": meal.meal_name,
                "servings": meal.servings,
                "nutrients": meal.nutrients,
                "ingredients": meal.ingredients,
                "instructions": meal.instructions,
                "total_calories": meal.total_calories,
                "calories_unit": meal.calories_unit,
                "created_on": meal.created_on,
            })

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
