from sqlalchemy.orm import Session
from abstractions.dependency import IDependency

from services.apis.v1.meal.history import FetchMealHistoryService

from repositories.meal_log import MealLogRepository

from start_utils import db_session


class FetchMealHistoryDependency(IDependency):

    @staticmethod
    def derive(
        urn: str,
        user_urn: str,
        api_name: str,
        user_id: str,
        session: Session = db_session,
    ) -> FetchMealHistoryService:
        return FetchMealHistoryService(
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
