from sqlalchemy.orm import Session
from abstractions.dependency import IDependency

from services.apis.meal.fetch import FetchMealService

from repositories.meal_log import MealLogRepository

from start_utils import db_session


class FetchMealDependency(IDependency):

    def __init__(self, urn: str, user_urn: str, api_name: str) -> None:
        super().__init__(urn, user_urn, api_name)

    def derive(
        self,
        urn: str,
        user_urn: str,
        api_name: str,
        user_id: str,
        session: Session = db_session,
    ) -> FetchMealService:
        return FetchMealService(
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
