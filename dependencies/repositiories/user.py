from typing import Callable

from repositories.user import UserRepository


class UserRepositoryDependency:

    @staticmethod
    def derive() -> Callable:
        def factory(
            urn,
            user_urn,
            api_name,
            session,
        ):
            return UserRepository(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                session=session,
            )
        return factory
