from http import HTTPStatus

from constants.api_status import APIStatus

from errors.bad_input_error import BadInputError

from dtos.responses.base import BaseResponseDTO

from models.user import User

from repositories.user import UserRepository

from services.user.abstraction import IUserService

from start_utils import db_session

from utilities.jwt import JWTUtility


class UserLogoutService(IUserService):

    def __init__(
        self, urn: str = None, user_urn: str = None, api_name: str = None
    ) -> None:
        super().__init__(urn, user_urn, api_name)
        self._urn = urn
        self._user_urn = user_urn
        self._api_name = api_name
        self._user_repository = UserRepository(
            urn=self._urn,
            user_urn=self._user_urn,
            api_name=self._api_name,
            session=db_session,
        )
        self._jwt_utility = JWTUtility(urn=self._urn)

    @property
    def urn(self):
        return self._urn

    @urn.setter
    def urn(self, value):
        self._urn = value

    @property
    def user_urn(self):
        return self._user_urn

    @user_urn.setter
    def user_urn(self, value):
        self._user_urn = value

    @property
    def api_name(self):
        return self._api_name

    @api_name.setter
    def api_name(self, value):
        self._api_name = value

    @property
    def user_repository(self):
        return self._user_repository

    @user_repository.setter
    def user_repository(self, value):
        self._user_repository = value

    @property
    def jwt_utility(self):
        return self._jwt_utility

    @jwt_utility.setter
    def jwt_utility(self, value):
        self._jwt_utility = value

    async def run(self, data: dict) -> dict:

        self.logger.debug("Fetching user")
        user: User = self.user_repository.retrieve_record_by_id_is_logged_in(
            id=data.get("user_id"), is_logged_in=True
        )
        self.logger.debug("Fetched user")

        if not user:
            raise BadInputError(
                responseMessage="User not Found. Incorrect user id.",
                responseKey="error_authorisation_failed",
                http_status_code=HTTPStatus.BAD_REQUEST,
            )

        self.logger.debug("Updating logged out status")
        user: User = self.user_repository.update_record(
            id=user.id,
            new_data={
                "is_logged_in": False,
            },
        )
        self.logger.debug("Updated logged out status")

        return BaseResponseDTO(
            transactionUrn=self.urn,
            status=APIStatus.SUCCESS,
            responseMessage="Successfully Logged Out the user.",
            responseKey="success_user_logout",
            data={"status": user.is_logged_in},
        )
