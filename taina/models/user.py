import psycopg.errors
import sqlalchemy

from .. import schemas
from ..core import postgres

User = sqlalchemy.Table(
    "user",
    postgres.metadata,
    sqlalchemy.Column("username", sqlalchemy.Text, primary_key=True),
    sqlalchemy.Column("password", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column("display_name", sqlalchemy.Text, nullable=True),
)


class UsernameInUse(Exception):
    pass


class UserDoesNotExist(Exception):
    pass


@postgres.session
async def user_create(session, user: schemas.UserCreate):
    query = User.insert().values(**user.model_dump()).returning(*User.c)

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
async def user_update(session, username: str, user: schemas.UserUpdate):
    query = User.update().where(
        User.c.username == username,
    ).values(
        **user.model_dump(),
    ).returning(*User.c)

    user = await session.fetch_one(query)

    if not user:
        raise UserDoesNotExist

    return user


@postgres.session
async def user_delete(session, username: str):
    query = User.delete().where(User.c.username == username)
    await session.execute(query)
