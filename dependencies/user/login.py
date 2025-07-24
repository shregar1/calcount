from sqlalchemy.orm import Session
from abstractions.dependency import IDependency

from services.user.login import UserLoginService

from repositories.user import UserRepository

from start_utils import db_session


class UserLoginDependency(IDependency):

    def __init__(self, urn: str, user_urn: str, api_name: str) -> None:
        super().__init__(urn, user_urn, api_name)

    def derive(
        self,
        urn: str,
        user_urn: str,
        api_name: str,
        user_id: str,
        session: Session = db_session,
    ) -> UserLoginService:
        return UserLoginService(
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            user_id=user_id,
            user_repository=UserRepository(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                session=session,
            ),
        )
