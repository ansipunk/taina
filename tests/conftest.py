import uuid

import alembic
import alembic.config
import async_asgi_testclient
import psycopg
import psycopg.sql
import pytest

import taina
import taina.core.config
import taina.core.postgres
import taina.models
import taina.schemas


@pytest.fixture(scope="session", autouse=True)
def _prepare_test_database(worker_id):
    url = taina.core.config.postgres.url

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

    worker_id = int(worker_id[2:]) + 1
    taina.core.config.redis.db = worker_id
    taina.core.config.redis.force_rollback = True

    yield

    query = psycopg.sql.SQL("DROP DATABASE {0};").format(database_sql)
    cursor.execute(query)
    cursor.close()
    connection.close()


@pytest.fixture()
async def _postgres():
    await taina.core.postgres.connect(taina.core.config.postgres.url)
    yield
    await taina.core.postgres.disconnect()


@pytest.fixture()
async def _redis():
    await taina.core.redis.connect(
        taina.core.config.redis.url,
        db=taina.core.config.redis.db,
    )
    yield
    await taina.core.redis.disconnect()


@pytest.fixture()
def user(_postgres):
    async def builder(
        username: str = "username",
        password: str = "P@ssw0rd",
        display_name: str = "Display Name",
    ) -> dict:
        return await taina.models.user_create(
            taina.schemas.UserCreate(
                username=username,
                password=password,
                display_name=display_name,
            ),
        )

    return builder


@pytest.fixture()
def user_default_credentials():
    return "johndoe", "P@ssw0rd"


@pytest.fixture()
async def user_default(user, user_default_credentials):
    username, password = user_default_credentials
    return await user(username=username, password=password, display_name="John Doe")


@pytest.fixture()
async def api_client():
    async with async_asgi_testclient.TestClient(taina.app) as client:
        yield client


@pytest.fixture()
async def auth_api_client(api_client, user_default, user_default_credentials):
    username, password = user_default_credentials

    response = await api_client.post(
        "/api/tokens/obtain",
        form={"username": username, "password": password},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    async with async_asgi_testclient.TestClient(
        taina.app,
        headers={"Authorization": f"Bearer {token}"},
    ) as client:
        yield client
