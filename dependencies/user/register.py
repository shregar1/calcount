from typing import Callable

from abstractions.dependency import IDependency

from services.user.registration import UserRegistrationService

from repositories.user import UserRepository

from start_utils import db_session


class UserRegistrationDependency(IDependency):

    @staticmethod
    def derive() -> Callable:
        def factory(
            urn,
            user_urn,
            api_name,
            user_id,
            session=db_session,
        ):
            return UserRegistrationService(
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
        return factory
