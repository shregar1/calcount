import jwt

from datetime import datetime, timedelta
from jwt import PyJWTError
from typing import Dict, Union

from abstractions.utility import IUtility

from start_utils import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


class JWTUtility(IUtility):

    def __init__(
        self,
        urn: str = None,
        user_urn: str = None,
        api_name: str = None,
        user_id: str = None,
    ) -> None:
        super().__init__(
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            user_id=user_id,
        )
        self._urn: str = urn
        self._user_urn: str = user_urn
        self._api_name: str = api_name
        self._user_id: str = user_id

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
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    def create_access_token(self, data: dict) -> str:

        to_encode = data.copy()
        if ACCESS_TOKEN_EXPIRE_MINUTES:
            expire = datetime.now() + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        else:
            expire = datetime.now() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    def decode_token(self, token: str) -> Union[Dict[str, str]]:
        try:

            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload

        except PyJWTError as err:
            raise err
