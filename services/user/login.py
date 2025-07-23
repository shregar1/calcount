import bcrypt
import os

from datetime import datetime
from http import HTTPStatus

from abstractions.service import IService

from constants.api_status import APIStatus

from errors.bad_input_error import BadInputError

from dtos.responses.base import BaseResponseDTO

from models.user import User

from repositories.user import UserRepository

from start_utils import db_session, user_type_lk_global_context_by_name

from utilities.jwt import JWTUtility


class UserLoginService(IService):

    def __init__(
        self, urn: str = None, user_urn: str = None, api_name: str = None
    ) -> None:
        super().__init__(urn, user_urn, api_name)
        self.urn = urn
        self.user_urn = user_urn
        self.api_name = api_name

        self.jwt_utility = JWTUtility(urn=self.urn)
        self.user_repository = UserRepository(
            urn=self.urn,
            user_urn=self.user_urn,
            api_name=self.api_name,
            session=db_session,
        )

    async def run(self, data: dict) -> dict:

        self.logger.debug("Fetching user")
        user: User = (
            self.user_repository.retrieve_record_by_email_user_type_id(
                email=data.get("email"),
                user_type_id=user_type_lk_global_context_by_name.get(
                    data.get("user_type")
                ).id,
                is_deleted=False,
            )
        )
        self.logger.debug("Fetched user")

        if not user:
            raise BadInputError(
                responseMessage="User not Found. Incorrect email.",
                responseKey="error_authorisation_failed",
                http_status_code=HTTPStatus.BAD_REQUEST,
            )

        if user.password != bcrypt.hashpw(
            data.get("password").encode("utf8"),
            os.getenv("BCRYPT_SALT").encode("utf8"),
        ).decode("utf8"):
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
                "status": user.is_logged_in,
                "token": token,
                "user_urn": user.urn,
            },
        )
