from typing import Callable

from abstractions.dependency import IDependency

from services.apis.meal.add import AddMealService

from repositories.meal_log import MealLogRepository

from start_utils import db_session


class AddMealDependency(IDependency):

    @staticmethod
    def derive() -> Callable:
        def factory(
            urn,
            user_urn,
            api_name,
            user_id,
            session=db_session
        ):
            return AddMealService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                meal_log_repository=MealLogRepository(
                    urn=urn,
                    user_urn=user_urn,
                    api_name=api_name,
                    session=session,
                ),
            )
        return factory
