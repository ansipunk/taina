import psycopg.errors
import sqlalchemy

from ..core import postgres

User = sqlalchemy.Table(
    "user",
    postgres.metadata,
    sqlalchemy.Column("username", sqlalchemy.Text, primary_key=True),
    sqlalchemy.Column("password", sqlalchemy.Text, nullable=False),
)


class UsernameInUse(Exception):
    pass


class UserDoesNotExist(Exception):
    pass


@postgres.session
async def user_create(session, username: str, password: str):
    query = User.insert().values(
        username=username,
        password=password,
    ).returning(*User.c)

    try:
        user = await session.fetch_one(query)
    except psycopg.errors.UniqueViolation as e:
        raise UsernameInUse from e

    return user


@postgres.session
async def user_get(session, username: str):
    query = User.select().where(User.c.username == username)
    user = await session.fetch_one(query)

    if not user:
        raise UserDoesNotExist

    return user


@postgres.session
async def user_list(session):
    query = User.select()
    return await session.fetch_all(query)


@postgres.session
async def user_update(session, username: str, password: str):
    query = User.update().where(
        User.c.username == username,
    ).values(
        password=password,
    ).returning(*User.c)

    user = await session.fetch_one(query)

    if not user:
        raise UserDoesNotExist

    return user


@postgres.session
async def user_delete(session, username: str):
    query = User.delete().where(User.c.username == username)
    await session.execute(query)
