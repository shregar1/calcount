import collections

from redis import Redis

from constants.api_status import APIStatus

from dtos.requests.apis.v1.meal.history import FetchMealHistoryRequestDTO
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
        meal_log_repository: MealLogRepository = None,
        cache: Redis = None,
    ) -> None:
        super().__init__(urn, user_urn, api_name)
        self._urn = urn
        self._user_urn = user_urn
        self._api_name = api_name
        self._user_id = user_id
        self._meal_log_repository = meal_log_repository
        self._cache = cache
        self.logger.debug(
            f"FetchMealHistoryService initialized for "
            f"user_id={user_id}, urn={urn}, api_name={api_name}"
        )

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

    @property
    def cache(self):
        return self._cache

    @cache.setter
    def cache(self, value):
        self._cache = value

    async def run(
        self,
        request_dto: FetchMealHistoryRequestDTO
    ) -> BaseResponseDTO:
        """
        Fetch the meal history for the user.
        Args:
            request_dto (FetchMealHistoryRequestDTO): The request DTO
            containing the from_date and to_date.
        Returns:
            BaseResponseDTO: The response DTO with meal history data.
        """

        from_date = request_dto.from_date
        to_date = request_dto.to_date

        self.logger.info(
            f"Fetching meal history for user_id={self.user_id}"
        )
        meal_history = (
            self.meal_log_repository.retrieve_history_by_user_id_date_range(
                user_id=self.user_id,
                from_date=from_date,
                to_date=to_date,
                is_deleted=False
            )
        )

        if not meal_history:
            self.logger.info("No meal history found")
            return BaseResponseDTO(
                transactionUrn=self.urn,
                status=APIStatus.SUCCESS,
                responseMessage="No meal history found.",
                responseKey="error_no_meal_history",
                data=None,
            )
        self.logger.info(
            f"Fetched {len(meal_history) if meal_history else 0} meal records"
        )

        meal_history_data = collections.defaultdict(list)
        for meal in meal_history:
            self.logger.debug(
                f"Processing meal: {meal.meal_name} "
                f"(servings: {meal.servings})"
            )
            meal_history_data[str(meal.created_on.date())].append({
                "meal_name": meal.meal_name,
                "servings": meal.servings,
                "nutrients": meal.nutrients,
                "ingredients": meal.ingredients,
                "instructions": meal.instructions,
                "total_calories": meal.total_calories,
                "calories_unit": meal.calories_unit,
                "created_on": str(meal.created_on),
                "source": "usda"
            })

        data = dict(meal_history_data)

        self.logger.info("Returning meal history response")
        return BaseResponseDTO(
            transactionUrn=self.urn,
            status=APIStatus.SUCCESS,
            responseMessage="Successfully fetched the meal history.",
            responseKey="success_fetch_meal",
            data=data,
        )
