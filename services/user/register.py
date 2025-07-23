import bcrypt
import os
import ulid

from datetime import datetime
from http import HTTPStatus

from abstractions.service import IService

from constants.api_status import APIStatus

from errors.bad_input_error import BadInputError

from dtos.responses.base import BaseResponseDTO

from models.user import User

from repositories.user import UserRepository

from start_utils import db_session, user_type_lk_global_context_by_name


class UserRegistrationService(IService):

    def __init__(
        self, urn: str = None, user_urn: str = None, api_name: str = None
    ) -> None:
        super().__init__(urn, user_urn, api_name)
        self.urn = urn
        self.user_urn = user_urn
        self.api_name = api_name

        self.user_repository = UserRepository(
            urn=self.urn,
            user_urn=self.user_urn,
            api_name=self.api_name,
            session=db_session,
        )

    async def run(self, data: dict) -> dict:

        self.logger.debug("Checking if user exists")
        user: User = self.user_repository.retrieve_record_by_email(
            email=data.get("email")
        )

        if user:

            self.logger.debug("User already exists")
            raise BadInputError(
                responseMessage="Email already registered. Please choose a different email address.",
                responseKey="error_email_already_registered",
                http_status_code=HTTPStatus.BAD_REQUEST,
            )

        self.logger.debug("Preparing user data")
        user: User = User(
            urn=ulid.ulid(),
            email=data.get("email"),
            password=bcrypt.hashpw(
                data.get("password").encode("utf-8"),
                os.getenv("BCRYPT_SALT").encode("utf8"),
            ).decode("utf8"),
            user_type_id=user_type_lk_global_context_by_name.get(
                data.get("user_type")
            ).id,
            is_deleted=False,
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
