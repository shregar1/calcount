from typing import Callable

from utilities.dictionary import DictionaryUtility


class DictionaryUtilityDependency:

    @staticmethod
    def derive() -> Callable:
        def factory(urn: str):
            return DictionaryUtility(urn=urn)
        return factory
