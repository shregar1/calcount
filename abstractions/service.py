from abc import ABC, abstractmethod
from pydantic import BaseModel

from start_utils import logger


class IService(ABC):

    def __init__(
        self,
        urn: str = None,
        user_urn: str = None,
        api_name: str = None,
        user_id: int = None,
    ) -> None:
        self.urn = urn
        self.user_urn = user_urn
        self.api_name = api_name
        self.logger = logger.bind(
            urn=self.urn, user_urn=self.user_urn, api_name=self.api_name
        )

    @abstractmethod
    def run(self, data: BaseModel) -> dict:
        pass
