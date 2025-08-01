"""schema

Revision ID: 31c7fc3c6b39
Revises: 31c7fc3c6b39
Create Date: 2025-07-23 19:39:15.685160

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31c7fc3c6b39'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'user',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('urn', sa.String, nullable=False, index=True),
        sa.Column('email', sa.String, unique=True, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('is_deleted', sa.Boolean, nullable=False, default=False),
        sa.Column('last_login', sa.DateTime(timezone=True)),
        sa.Column('is_logged_in', sa.Boolean, nullable=False, default=False),
        sa.Column('created_on', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_by', sa.BigInteger, nullable=False),
        sa.Column('updated_on', sa.DateTime(timezone=True)),
        sa.Column('updated_by', sa.BigInteger),
    )
    op.execute("""CREATE INDEX IF NOT EXISTS ix_user_urn ON
    "user" (urn)""")
    op.execute("""CREATE INDEX IF NOT EXISTS ix_user_email ON
    "user" (email)""")
    op.execute("""CREATE INDEX IF NOT EXISTS ix_user_last_login ON
    "user" (last_login)""")
    op.execute("""CREATE INDEX IF NOT EXISTS ix_user_is_logged_in ON
    "user" (is_logged_in)""")

    op.create_table(
        'meal_log',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('urn', sa.String, nullable=False, index=True),
        sa.Column('user_id', sa.BigInteger, nullable=False),
        sa.Column('meal_name', sa.String, nullable=False),
        sa.Column('servings', sa.Integer, nullable=False),
        sa.Column('nutrients', sa.JSON, nullable=False),
        sa.Column('ingredients', sa.JSON, nullable=False),
        sa.Column('instructions', sa.JSON, nullable=False),
        sa.Column('total_calories_per_serving', sa.Integer, nullable=False),
        sa.Column('calories_unit', sa.String, nullable=False),
        sa.Column('total_calories', sa.Integer, nullable=False),
        sa.Column('is_deleted', sa.Boolean, nullable=False, default=False),
        sa.Column('created_on', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_by', sa.BigInteger, nullable=False),
        sa.Column('updated_on', sa.DateTime(timezone=True)),
        sa.Column('updated_by', sa.BigInteger),
    )
    op.execute(
        """CREATE INDEX IF NOT EXISTS ix_meal_log_urn ON
        "meal_log" (urn)"""
    )
    op.execute(
        """CREATE INDEX IF NOT EXISTS ix_meal_log_user_id ON
        "meal_log" (user_id)"""
    )
    op.execute(
        """CREATE INDEX IF NOT EXISTS ix_meal_log_meal_name ON
        "meal_log" (meal_name)"""
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('meal_log')
    op.drop_table('user')
