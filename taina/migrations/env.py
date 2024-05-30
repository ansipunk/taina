import alembic.context
import sqlalchemy
import sqlalchemy.pool

from taina import models  # noqa: F401
from taina.core import config
from taina.core import postgres


def run_migrations() -> None:
    engine = sqlalchemy.create_engine(config.postgres.url)

    with engine.connect() as connection:
        alembic.context.configure(
            connection=connection,
            target_metadata=postgres.metadata,
        )

        with alembic.context.begin_transaction():
            alembic.context.run_migrations()

    engine.dispose()


run_migrations()
