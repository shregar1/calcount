from typing import Callable

from abstractions.dependency import IDependency

from services.user.logout import UserLogoutService


class UserLogoutServiceDependency(IDependency):

    @staticmethod
    def derive() -> Callable:
        def factory(
            urn,
            user_urn,
            api_name,
            user_id,
            jwt_utility,
            user_repository,
        ):
            return UserLogoutService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                user_repository=user_repository,
                jwt_utility=jwt_utility,
            )
        return factory
