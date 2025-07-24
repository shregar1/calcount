from datetime import datetime
from sqlalchemy import (
    Column,
    BigInteger,
    String,
    DateTime,
    Boolean,
    Index,
)

from constants.db.table import Table

from models import Base


class User(Base):

    __tablename__ = Table.USER

    id = Column(BigInteger, primary_key=True)
    urn = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    last_login = Column(DateTime(timezone=True))
    is_logged_in = Column(Boolean, nullable=False, default=False)
    created_on = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        default=datetime.utcnow
    )
    created_by = Column(BigInteger, nullable=False)
    updated_on = Column(DateTime(timezone=True))
    updated_by = Column(BigInteger)


Index('ix_user_urn', User.urn)
Index('ix_user_email', User.email, unique=True)
Index('ix_user_created_on', User.created_on)
