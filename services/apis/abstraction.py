from pydantic import BaseModel

from abstractions.service import IService

from dtos.responses.base import BaseResponseDTO


class IAPIService(IService):

    def __init__(
        self,
        urn: str = None,
        user_urn: str = None,
        api_name: str = None,
        user_id: int = None,
    ) -> None:
        super().__init__(urn, user_urn, api_name, user_id)

    def run(self, request_dto: BaseModel) -> BaseResponseDTO:
        pass
