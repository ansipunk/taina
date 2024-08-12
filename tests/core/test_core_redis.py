import pytest

import taina.core.redis


@pytest.mark.usefixtures("_redis")
async def test_use_session():
    async with taina.core.redis.Session() as session:
        await session.ping()


async def test_use_session_without_redis_connection():
    with pytest.raises(taina.core.redis.RedisNotConnectedError):
        async with taina.core.redis.Session():
            pass


async def test_use_session_without_acquired_connection():
    session = taina.core.redis.Session()

    with pytest.raises(taina.core.redis.ConnectionNotAcquiredError):
        await session.ping()
