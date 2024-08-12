import pytest

import taina.core.postgres
import taina.models


@pytest.mark.usefixtures("_postgres")
async def test_use_session():
    async with taina.core.postgres.Session() as session:
        query = taina.models.User.select()
        await session.fetch_all(query)


async def test_use_session_without_postgres_connection():
    with pytest.raises(taina.core.postgres.PostgresNotConnectedError):
        async with taina.core.postgres.Session():
            pass


async def test_use_session_without_acquired_connection():
    session = taina.core.postgres.Session()
    query = taina.models.User.select()

    with pytest.raises(taina.core.postgres.ConnectionNotAcquiredError):
        await session.fetch_all(query)


@pytest.mark.usefixtures("_postgres")
async def test_use_session_transaction():
    username = "username"
    password = "password"

    async with taina.core.postgres.Session() as session:
        async with session.transaction():
            query = taina.models.User.insert().values(
                username=username,
                password=password,
            )
            await session.execute(query)

        query = taina.models.User.select().where(
            taina.models.User.c.username == username,
        )
        user = await session.fetch_one(query)

    assert user["username"] == username
    assert user["password"] == password


@pytest.mark.usefixtures("_postgres")
async def test_use_session_transaction_rollback():
    username = "username"
    password = "password"

    async with taina.core.postgres.Session() as session:
        with pytest.raises(RuntimeError):  # noqa: PT012
            async with session.transaction():
                query = taina.models.User.insert().values(
                    username=username,
                    password=password,
                )
                await session.execute(query)
                raise RuntimeError

        query = taina.models.User.select().where(
            taina.models.User.c.username == username,
        )
        user = await session.fetch_one(query)

    assert user is None


@pytest.mark.usefixtures("_postgres")
async def test_use_session_transaction_without_acquired_connection():
    session = taina.core.postgres.Session()

    with pytest.raises(taina.core.postgres.ConnectionNotAcquiredError):
        async with session.transaction():
            pass
