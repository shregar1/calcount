from typing import Callable

from utilities.jwt import JWTUtility


class JWTUtilityDependency:

    @staticmethod
    def derive() -> Callable:
        def factory(
            urn: str,
            user_urn: str,
            api_name: str,
            user_id: str,
        ):
            return JWTUtility(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
            )
        return factory
