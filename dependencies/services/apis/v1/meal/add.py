from typing import Callable

from abstractions.dependency import IDependency

from services.apis.v1.meal.add import AddMealService

from start_utils import logger


class AddMealServiceDependency(IDependency):
    """
    Dependency provider for AddMealService.
    Provides a factory for creating AddMealService instances with DI.
    """
    @staticmethod
    def derive() -> Callable:
        """
        Returns a factory function that creates an AddMealService with the
        given parameters.
        Logs when the factory is created and when a service is instantiated.
        """
        logger.debug("AddMealServiceDependency factory created")

        def factory(
            urn,
            user_urn,
            api_name,
            user_id,
            meal_log_repository,
            cache,
        ):
            logger.info(
                "Instantiating AddMealService"
            )
            return AddMealService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                meal_log_repository=meal_log_repository,
                cache=cache,
            )
        return factory
