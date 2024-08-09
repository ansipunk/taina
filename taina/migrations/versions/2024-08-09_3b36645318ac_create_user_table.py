"""Create user table

Revision ID: 3b36645318ac
Revises:
Create Date: 2024-08-09 20:20:01.333987+00:00
"""

import alembic.op
import sqlalchemy

revision = "3b36645318ac"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    alembic.op.create_table(
        "user",
        sqlalchemy.Column("username", sqlalchemy.Text(), nullable=False),
        sqlalchemy.Column("password", sqlalchemy.Text(), nullable=False),
        sqlalchemy.Column("display_name", sqlalchemy.Text(), nullable=True),
        sqlalchemy.PrimaryKeyConstraint("username"),
    )


def downgrade():
    alembic.op.drop_table("user")
