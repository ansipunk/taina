from ..core import redis


class TokenDoesNotExist(Exception):
    pass


@redis.session
async def access_token_set(
    session,
    username: str,
    access_token: str,
    refresh_token: str,
    ttl: int | None = None,
) -> str:
    await session.set(f"tokens:{refresh_token}:{access_token}", username, ex=ttl)
    return access_token


@redis.session
async def access_token_get(session, access_token: str) -> str:
    keys = await session.keys(f"tokens:*:{access_token}")

    for key in keys:
        username = await session.get(key)

        if username:
            return username.decode("utf-8")

    raise TokenDoesNotExist


@redis.session
async def refresh_token_set(
    session,
    username: str,
    refresh_token: str,
    ttl: int | None = None,
) -> str:
    await session.set(f"tokens:{refresh_token}", username, ex=ttl)
    return refresh_token


@redis.session
async def refresh_token_get(session, refresh_token: str) -> str:
    username = await session.get(f"tokens:{refresh_token}")

    if not username:
        raise TokenDoesNotExist

    return username.decode("utf-8")


@redis.session
async def refresh_token_del(session, refresh_token: str):
    keys = await session.keys(f"tokens:{refresh_token}*")

    for key in keys:
        await session.delete(key)


@redis.session
async def refresh_token_get_by_access_token(session, access_token: str) -> str:
    keys = await session.keys(f"tokens:*:{access_token}")

    for key in keys:
        _, refresh_token, _ = key.split(b":")
        return refresh_token.decode("utf-8")

    return None
