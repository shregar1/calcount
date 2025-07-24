import bcrypt
import os
import ulid

from datetime import datetime
from http import HTTPStatus

from abstractions.service import IService

from constants.api_status import APIStatus

from dtos.requests.user.registration import UserRegistrationRequestDTO
from dtos.responses.base import BaseResponseDTO

from errors.bad_input_error import BadInputError

from models.user import User

from repositories.user import UserRepository


class UserRegistrationService(IService):

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

        self.user_repository = user_repository

    async def run(self, request_dto: UserRegistrationRequestDTO) -> dict:

        self.logger.debug("Checking if user exists")
        user: User = self.user_repository.retrieve_record_by_email(
            email=request_dto.email
        )

        if user:

            self.logger.debug("User already exists")
            raise BadInputError(
                responseMessage="Email already registered.",
                responseKey="error_email_already_registered",
                http_status_code=HTTPStatus.BAD_REQUEST,
            )

        self.logger.debug("Preparing user data")
        user: User = User(
            urn=ulid.ulid(),
            email=request_dto.email,
            password=bcrypt.hashpw(
                request_dto.password.encode("utf-8"),
                os.getenv("BCRYPT_SALT").encode("utf8"),
            ).decode("utf8"),
            is_deleted=False,
            created_by=1,
            created_on=datetime.now(),
        )

        user: User = self.user_repository.create_record(user=user)
        self.logger.debug("Preparing user data")

        return BaseResponseDTO(
            transactionUrn=self.urn,
            status=APIStatus.SUCCESS,
            responseMessage="Successfully registered the user.",
            responseKey="success_user_register",
            data={
                "user_email": user.email,
                "created_at": str(user.created_on),
            },
        )
