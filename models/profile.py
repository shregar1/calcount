from datetime import datetime
from sqlalchemy import (
    Column,
    BigInteger,
    String,
    DateTime,
    Boolean,
    Index,
    ForeignKey,
    Date,
)
from sqlalchemy.dialects.postgresql import BIGSERIAL
from sqlalchemy.orm import relationship

from constants.db.table import Table

from models import Base
from models.user import User


class Profile(Base):

    __tablename__ = Table.PROFILE

    id = Column(BIGSERIAL, primary_key=True)
    urn = Column(String, nullable=False, index=True)
    user_id = Column(
        BigInteger,
        ForeignKey(User.id),
        nullable=False,
        unique=True,
        index=True
    )
    first_name = Column(String, nullable=False)
    middle_name = Column(String)
    last_name = Column(String)
    gender_id = Column(BigInteger, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    height_cm = Column(BigInteger)
    weight_kg = Column(BigInteger)
    smoking_habits_id = Column(BigInteger)
    drinking_habits_id = Column(BigInteger)
    exercise_habits_id = Column(BigInteger)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_on = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        default=datetime.utcnow
    )
    created_by = Column(BigInteger, nullable=False)
    updated_on = Column(DateTime(timezone=True))
    updated_by = Column(BigInteger)

    # Relationship to user
    user = relationship("User", back_populates="profile")


Index('ix_profile_urn', Profile.urn)
Index('ix_profile_user_id', Profile.user_id, unique=True)
Index('ix_profile_created_on', Profile.created_on)
