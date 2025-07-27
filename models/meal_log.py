"""
SQLAlchemy model for the meal_log table, representing user meal logs and their
nutritional details.
"""
from datetime import datetime
from sqlalchemy import (
    Column,
    BigInteger,
    String,
    DateTime,
    Boolean,
    Index,
    Integer,
    JSON,
    ForeignKey
)

from constants.db.table import Table

from models import Base
from models.user import User


class MealLog(Base):
    """
    SQLAlchemy model for a meal log entry.
    Fields:
        id (BigInteger): Primary key.
        urn (str): Unique resource name for the meal log.
        user_id (BigInteger): Foreign key to User.id.
        meal_name (str): Name of the meal.
        servings (int): Number of servings.
        nutrients (JSON): Nutritional information.
        ingredients (JSON): List of ingredients.
        instructions (JSON): Cooking instructions.
        total_calories_per_serving (int): Calories per serving.
        calories_unit (str): Unit for calories.
        total_calories (int): Total calories for the meal.
        is_deleted (bool): Soft delete flag.
        created_on (datetime): Creation timestamp.
        created_by (BigInteger): Creator's user ID.
        updated_on (datetime): Last update timestamp.
        updated_by (BigInteger): Last updater's user ID.
    """
    __tablename__ = Table.MEAL_LOG

    id = Column(BigInteger, primary_key=True)
    urn = Column(String, nullable=False, index=True)
    user_id = Column(
        BigInteger,
        ForeignKey(User.id),
        nullable=False,
        unique=True,
        index=True
    )
    meal_name = Column(String, index=True)
    servings = Column(Integer)
    nutrients = Column(JSON)
    ingredients = Column(JSON)
    instructions = Column(JSON)
    total_calories_per_serving = Column(Integer)
    calories_unit = Column(String)
    total_calories = Column(Integer)
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


Index('ix_meal_log_urn', MealLog.urn)
Index('ix_meal_log_meal_name', MealLog.meal_name)
Index('ix_meal_log_created_on', MealLog.created_on)
