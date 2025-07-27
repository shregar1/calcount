from typing import List
from datetime import date, timedelta

from redis import Redis

from constants.api_status import APIStatus

from dtos.requests.apis.v1.meal.recommendation import (
    FetchMealRecommendationRequestDTO
)
from dtos.responses.base import BaseResponseDTO
from dtos.services.apis.v1.meal.recommendation import MealRecommendationDTO

from models.meal_log import MealLog
from repositories.meal_log import MealLogRepository

from services.apis.v1.meal.abstraction import IMealAPIService


class FetchMealRecommendationService(IMealAPIService):

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

    async def process_meal_recommendation(
        self,
        meal_history: List[MealLog],
        food_category: str
    ) -> MealRecommendationDTO:

        self.logger.info(
            f"Generating meal recommendations for category: {food_category}"
        )

        meal_history_data = []
        for meal in meal_history:
            meal_history_data.append({
                "meal_name": meal.meal_name,
                "servings": meal.servings,
                "nutrients": meal.nutrients,
                "ingredients": meal.ingredients,
            })

        meal_recommendation_data = await self.generate_meal_recommendation(
            food_category=food_category,
            meal_history=meal_history_data
        )
        self.logger.info("Meal recommendations generated")
        return meal_recommendation_data

    async def run(
        self,
        request_dto: FetchMealRecommendationRequestDTO
    ) -> BaseResponseDTO:

        self.logger.info(
            f"Fetching meal history for user_id={self.user_id} within"
            f" the last 7 days"
        )
        from_date = date.today()
        to_date = date.today() - timedelta(days=7)
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
            meal_history = []
        self.logger.info(
            f"Fetched {len(meal_history) if meal_history else 0} meal records"
        )

        self.logger.info("Generating meal recommendations")
        recommendations_dto = await self.process_meal_recommendation(
            meal_history, request_dto.food_category)
        recommendations_data = recommendations_dto.model_dump()
        self.logger.info("Meal recommendations generated")

        return BaseResponseDTO(
            transactionUrn=self.urn,
            status=APIStatus.SUCCESS,
            responseMessage="Successfully fetched the meal recommendations.",
            responseKey="success_fetch_meal_recommendations",
            data=recommendations_data,
        )
