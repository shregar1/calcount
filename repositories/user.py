from datetime import datetime
from sqlalchemy.orm import Session

from models.user import User

from abstractions.repository import IRepository


class UserRepository(IRepository):

    def __init__(
        self,
        urn: str = None,
        user_urn: str = None,
        api_name: str = None,
        session: Session = None,
    ):
        super().__init__(urn, user_urn, api_name)
        self._urn = urn
        self._user_urn = user_urn
        self._api_name = api_name
        self._session = session
        if not self._session:
            raise RuntimeError("DB session not found")

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
    def session(self):
        return self._session

    @session.setter
    def session(self, value):
        if not isinstance(value, Session):
            raise ValueError("session must be a SQLAlchemy Session instance")
        self._session = value

    def create_record(
        self,
        user: User,
    ) -> User:

        start_time = datetime.now()
        self._session.add(user)
        self._session.commit()

        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return user

    def retrieve_record_by_email_and_password(
        self,
        email: str,
        password: str,
        is_deleted: bool = False,
    ) -> User:

        start_time = datetime.now()
        record = (
            self._session.query(User)
            .filter(
                User.email == email,
                User.password == password,
                User.is_deleted == is_deleted,
            )
            .first()
        )
        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return record if record else None

    def retrieve_record_by_email(
        self,
        email: str,
        is_deleted: bool = False,
    ) -> User:

        start_time = datetime.now()
        record = (
            self._session.query(User)
            .filter(User.email == email, User.is_deleted == is_deleted)
            .first()
        )
        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return record if record else None

    def retrieve_record_by_id(
        self,
        id: str,
        is_deleted: bool = False,
    ) -> User:

        start_time = datetime.now()
        record = (
            self._session.query(User)
            .filter(User.id == id, User.is_deleted == is_deleted)
            .first()
        )
        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return record if record else None

    def retrieve_record_by_urn(
        self,
        urn: str,
        is_deleted: bool = False,
    ) -> User:

        start_time = datetime.now()
        record = (
            self._session.query(User)
            .filter(User.urn == urn, User.is_deleted == is_deleted)
            .first()
        )
        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return record if record else None

    def retrieve_record_by_id_and_is_logged_in(
        self,
        id: str,
        is_logged_in: bool,
        is_deleted: bool = False,
    ) -> User:

        start_time = datetime.now()
        records = (
            self._session.query(User)
            .filter(
                User.id == id,
                User.is_logged_in == is_logged_in,
                User.is_deleted == is_deleted,
            )
            .all()
        )
        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return records

    def retrieve_record_by_id_is_logged_in(
        self,
        id: int,
        is_logged_in: bool,
        is_deleted: bool = False,
    ) -> User:

        start_time = datetime.now()
        record = (
            self._session.query(User)
            .filter(
                User.id == id,
                User.is_logged_in == is_logged_in,
                User.is_deleted == is_deleted,
            )
            .one_or_none()
        )
        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return record

    def update_record(
        self,
        id: str,
        new_data: dict,
    ) -> User:

        start_time = datetime.now()
        user = self._session.query(User).filter(User.id == id).first()

        if not user:
            raise ValueError(f"User with id {id} not found")

        for attr, value in new_data.items():
            setattr(user, attr, value)

        self._session.commit()
        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return user
