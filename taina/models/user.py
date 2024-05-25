import sqlalchemy

from ..core import postgres

User = sqlalchemy.Table(
    "user",
    postgres.metadata,
    sqlalchemy.Column("username", sqlalchemy.Text, primary_key=True),
    sqlalchemy.Column("password", sqlalchemy.Text, nullable=False),
)
