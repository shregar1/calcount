from sqlalchemy.orm import Session

from start_utils import db_session


class DBDependency:

    @staticmethod
    def derive() -> Session:
        return db_session
