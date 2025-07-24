import jwt

from datetime import datetime, timedelta
from jwt import PyJWTError
from typing import Dict, Union

from abstractions.utility import IUtility

from start_utils import (
    logger,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


class JWTUtility(IUtility):

    def __init__(self, urn: str = None) -> None:
        super().__init__(urn)
        self.urn = urn
        self.logger = logger

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
