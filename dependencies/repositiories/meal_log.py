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
            user_id,
        ):
            return MealLogRepository(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                session=session,
                user_id=user_id,
            )
        return factory
