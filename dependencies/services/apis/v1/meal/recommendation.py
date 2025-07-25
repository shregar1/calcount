from typing import Callable

from abstractions.dependency import IDependency

from services.apis.v1.meal.recommendation import FetchMealRecommendationService


class FetchMealRecommendationServiceDependency(IDependency):

    @staticmethod
    def derive() -> Callable:
        def factory(
            urn,
            user_urn,
            api_name,
            user_id,
            meal_log_repository,
        ):
            return FetchMealRecommendationService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                meal_log_repository=meal_log_repository,
            )
        return factory
