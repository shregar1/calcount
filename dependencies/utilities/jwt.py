from typing import Callable

from utilities.jwt import JWTUtility


class JWTUtilityDependency:

    @staticmethod
    def derive() -> Callable:
        def factory(urn: str):
            return JWTUtility(urn=urn)
        return factory
