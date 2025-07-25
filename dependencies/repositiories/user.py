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
            user_id,
        ):
            return UserRepository(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                session=session,
                user_id=user_id,
            )
        return factory
