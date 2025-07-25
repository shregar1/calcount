from typing import Callable

from abstractions.dependency import IDependency

from services.user.registration import UserRegistrationService


class UserRegistrationServiceDependency(IDependency):

    @staticmethod
    def derive() -> Callable:
        def factory(
            urn,
            user_urn,
            api_name,
            user_id,
            user_repository,
        ):
            return UserRegistrationService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                user_repository=user_repository,
            )
        return factory
