from typing import Callable

from repositories.meal_log import MealLogRepository
from start_utils import logger


class MealLogRepositoryDependency:
    """
    Dependency provider for MealLogRepository.
    Provides a factory for creating MealLogRepository instances with DI.
    """

    @staticmethod
    def derive() -> Callable:
        """
        Returns a factory function that creates a MealLogRepository with the
        given parameters.
        Logs when the factory is created and when a repository is instantiated.
        """
        logger.debug("MealLogRepositoryDependency factory created")

        def factory(
            urn,
            user_urn,
            api_name,
            session,
            user_id,
        ):
            logger.info(
                "Instantiating MealLogRepository"
            )
            return MealLogRepository(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                session=session,
                user_id=user_id,
            )
        return factory
