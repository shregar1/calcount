from typing import Callable

from abstractions.dependency import IDependency

from services.apis.v1.meal.fetch import FetchMealService

from start_utils import logger


class FetchMealServiceDependency(IDependency):
    """
    Dependency provider for FetchMealService.
    Provides a factory for creating FetchMealService instances with DI.
    """
    @staticmethod
    def derive() -> Callable:
        """
        Returns a factory function that creates a FetchMealService with the
        given parameters.
        Logs when the factory is created and when a service is instantiated.
        """
        logger.debug("FetchMealServiceDependency factory created")

        def factory(
            urn,
            user_urn,
            api_name,
            user_id,
            meal_log_repository,
            cache,
        ):
            logger.info(
                "Instantiating FetchMealService"
            )
            return FetchMealService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                meal_log_repository=meal_log_repository,
                cache=cache,
            )
        return factory
