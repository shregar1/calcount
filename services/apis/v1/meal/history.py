from constants.api_status import APIStatus

from dtos.requests.apis.v1.meal.fetch import FetchMealRequestDTO
from dtos.responses.base import BaseResponseDTO

from repositories.meal_log import MealLogRepository

from services.apis.v1.meal.abstraction import IMealAPIService


class FetchMealHistoryService(IMealAPIService):
    """
    Service to fetch meal history for a user.
    Provides a list of all meals logged by the user, including nutrients,
    ingredients, instructions, and calories.
    This service is used to fetch the meal history for a user.
    """

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
        """
        Fetch the meal history for the user.
        Args:
            request_dto (FetchMealRequestDTO): The request DTO containing
            request parameters.
        Returns:
            BaseResponseDTO: The response DTO with meal history data.
        """

        self.logger.info(
            f"Fetching meal history for user_id={self.user_id}"
        )
        meal_history = self.meal_log_repository.retrieve_history_by_user_id(
            user_id=self.user_id
        )
        self.logger.info(
            f"Fetched {len(meal_history) if meal_history else 0} meal records"
        )

        meal_history_data = []
        for meal in meal_history:
            self.logger.debug(
                f"Processing meal: {meal.meal_name} "
                f"(servings: {meal.servings})"
            )
            meal_history_data.append({
                "meal_name": meal.meal_name,
                "servings": meal.servings,
                "nutrients": meal.nutrients,
                "ingredients": meal.ingredients,
                "instructions": meal.instructions,
                "total_calories": meal.total_calories,
                "calories_unit": meal.calories_unit,
                "created_on": meal.created_on,
                "source": "usda"
            })

        self.logger.info("Returning meal history response")
        return BaseResponseDTO(
            transactionUrn=self.urn,
            status=APIStatus.SUCCESS,
            responseMessage="Successfully fetched the meal history.",
            responseKey="success_fetch_meal",
            data=meal_history_data,
        )
