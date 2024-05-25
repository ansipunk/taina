"""Create user table

Revision ID: 4de87a1261e7
Revises:
Create Date: 2024-05-25 15:44:33.261292+00:00
"""

import sqlalchemy as sa
from alembic import op

revision = "4de87a1261e7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("username", sa.Text(), nullable=False),
        sa.Column("password", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("username"),
    )


def downgrade():
    op.drop_table("user")
