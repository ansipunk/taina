import uuid

import alembic
import alembic.config
import psycopg
import psycopg.sql
import pytest

import taina.core.config
import taina.core.postgres
import taina.models


@pytest.fixture(scope="session", autouse=True)
def _prepare_test_database():
    url = taina.core.config.postgres.url.replace("postgresql+psycopg", "postgresql")

    database = f"taina_test_{uuid.uuid4()}"
    database_sql = psycopg.sql.Identifier(database)

    taina.core.config.postgres.database = database
    taina.core.config.postgres.force_rollback = True

    connection = psycopg.connect(url, autocommit=True)
    cursor = connection.cursor()
    query = psycopg.sql.SQL("CREATE DATABASE {0};").format(database_sql)
    cursor.execute(query)

    alembic_cfg = alembic.config.Config("alembic.ini")
    alembic.command.upgrade(alembic_cfg, "head")

    yield

    query = psycopg.sql.SQL("DROP DATABASE {0};").format(database_sql)
    cursor.execute(query)
    cursor.close()
    connection.close()


@pytest.fixture()
async def _db():
    await taina.core.postgres.connect(taina.core.config.postgres.url)
    yield
    await taina.core.postgres.disconnect()


@pytest.fixture()
def user(_db):
    async def builder(
        username: str = "username",
        password: str = "password",
    ) -> dict:
        return await taina.models.user_create(
            username=username,
            password=password,
        )

    return builder


@pytest.fixture()
async def user_default(user):
    return await user(username="default")
