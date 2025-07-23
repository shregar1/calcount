from abc import ABC, abstractmethod
from fastapi import Request
from fastapi.responses import JSONResponse

from start_utils import logger


class IController(ABC):

    def __init__(
        self, urn: str = None, user_urn: str = None, api_name: str = None
    ) -> None:
        super().__init__()
        self.urn = urn
        self.user_urn = user_urn
        self.api_name = api_name
        self.logger = logger.bind(urn=self.urn)

    async def validate_request(
        self,
        urn: str,
        user_urn: str,
        request_payload: dict,
        request_headers: dict,
        api_name: str,
        user_id: str,
    ):
        self.urn = urn
        self.user_urn = user_urn
        self.api_name = api_name
        self.user_id = user_id
        return

    @abstractmethod
    async def get(
        self,
        request: Request,
        request_payload: dict,
    ) -> JSONResponse:
        pass

    @abstractmethod
    async def post(
        self,
        request: Request,
        request_payload: dict,
    ) -> JSONResponse:
        pass

    @abstractmethod
    async def put(
        self,
        request: Request,
        request_payload: dict,
    ) -> JSONResponse:
        pass

    @abstractmethod
    async def delete(
        self,
        request: Request,
        request_payload: dict,
    ) -> JSONResponse:
        pass

    @abstractmethod
    async def patch(
        self,
        request: Request,
        request_payload: dict,
    ) -> JSONResponse:
        pass

    @abstractmethod
    async def options(
        self,
        request: Request,
        request_payload: dict,
    ) -> JSONResponse:
        pass
