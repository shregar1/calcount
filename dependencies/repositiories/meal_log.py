from typing import Callable

from repositories.meal_log import MealLogRepository


class MealLogRepositoryDependency:

    @staticmethod
    def derive() -> Callable:
        def factory(
            urn,
            user_urn,
            api_name,
            session,
        ):
            return MealLogRepository(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                session=session,
            )
        return factory
