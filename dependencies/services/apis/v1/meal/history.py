from typing import Callable

from abstractions.dependency import IDependency

from services.apis.v1.meal.history import FetchMealHistoryService


class FetchMealHistoryServiceDependency(IDependency):

    @staticmethod
    def derive() -> Callable:
        def factory(
            urn,
            user_urn,
            api_name,
            user_id,
            meal_log_repository,
            cache,
        ):
            return FetchMealHistoryService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                meal_log_repository=meal_log_repository,
                cache=cache,
            )
        return factory
