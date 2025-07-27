from typing import Callable

from abstractions.dependency import IDependency

from services.apis.v1.meal.history import FetchMealHistoryService

from start_utils import logger


class FetchMealHistoryServiceDependency(IDependency):
    """
    Dependency provider for FetchMealHistoryService.
    Provides a factory for creating FetchMealHistoryService instances with DI.
    """
    @staticmethod
    def derive() -> Callable:
        """
        Returns a factory function that creates a FetchMealHistoryService with
        the given parameters.
        Logs when the factory is created and when a service is instantiated.
        """
        logger.debug("FetchMealHistoryServiceDependency factory created")

        def factory(
            urn,
            user_urn,
            api_name,
            user_id,
            meal_log_repository,
            cache,
        ):
            logger.info(
                "Instantiating FetchMealHistoryService"
            )
            return FetchMealHistoryService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                meal_log_repository=meal_log_repository,
                cache=cache,
            )
        return factory
