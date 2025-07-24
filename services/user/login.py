import bcrypt

from datetime import datetime
from http import HTTPStatus

from abstractions.service import IService

from constants.api_status import APIStatus

from errors.bad_input_error import BadInputError
from errors.not_found_error import NotFoundError

from dtos.requests.user.login import UserLoginRequestDTO
from dtos.responses.base import BaseResponseDTO

from models.user import User

from repositories.user import UserRepository

from utilities.jwt import JWTUtility


class UserLoginService(IService):

    def __init__(
        self,
        urn: str = None,
        user_urn: str = None,
        api_name: str = None,
        user_id: int = None,
        user_repository: UserRepository = None,
    ) -> None:
        super().__init__(urn, user_urn, api_name)
        self.urn = urn
        self.user_urn = user_urn
        self.api_name = api_name
        self.user_id = user_id

        self.jwt_utility = JWTUtility(urn=self.urn)
        self.user_repository = user_repository

    async def run(self, request_dto: UserLoginRequestDTO) -> dict:

        self.logger.debug("Fetching user")
        user: User = (
            self.user_repository.retrieve_record_by_email(
                email=request_dto.email,
                is_deleted=False,
            )
        )
        self.logger.debug("Fetched user")

        if not user:
            raise NotFoundError(
                responseMessage="User not Found. Incorrect email.",
                responseKey="error_authorisation_failed",
                http_status_code=HTTPStatus.NOT_FOUND,
            )

        if not bcrypt.checkpw(
            request_dto.password.encode("utf8"),
            user.password.encode("utf8"),
        ):
            raise BadInputError(
                responseMessage="Incorrect password.",
                responseKey="error_authorisation_failed",
                http_status_code=HTTPStatus.BAD_REQUEST,
            )

        self.logger.debug("Updating logged in status")
        user: User = self.user_repository.update_record(
            id=user.id,
            new_data={
                "is_logged_in": True,
                "last_login": datetime.now(),
                "updated_on": datetime.now(),
            },
        )
        self.logger.debug("Updated logged in status")

        payload = {
            "user_id": user.id,
            "user_urn": user.urn,
            "user_email": user.email,
            "last_login": str(user.updated_on),
        }
        token: str = self.jwt_utility.create_access_token(data=payload)

        return BaseResponseDTO(
            transactionUrn=self.urn,
            status=APIStatus.SUCCESS,
            responseMessage="Successfully logged in the user.",
            responseKey="success_user_login",
            data={
                "status": True,
                "token": token,
                "user_urn": user.urn,
            },
        )
