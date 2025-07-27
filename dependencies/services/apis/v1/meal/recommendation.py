from typing import Callable

from abstractions.dependency import IDependency

from services.apis.v1.meal.recommendation import FetchMealRecommendationService

from start_utils import logger


class FetchMealRecommendationServiceDependency(IDependency):
    """
    Dependency provider for FetchMealRecommendationService.
    Provides a factory for creating FetchMealRecommendationService instances
    with DI.
    """
    @staticmethod
    def derive() -> Callable:
        """
        Returns a factory function that creates a
        FetchMealRecommendationService with the given parameters.
        Logs when the factory is created and when a service is instantiated.
        """
        logger.debug(
            "FetchMealRecommendationServiceDependency factory created"
        )

        def factory(
            urn,
            user_urn,
            api_name,
            user_id,
            meal_log_repository,
            cache,
        ):
            logger.info(
                "Instantiating FetchMealRecommendationService"
            )
            return FetchMealRecommendationService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                meal_log_repository=meal_log_repository,
                cache=cache,
            )
        return factory
