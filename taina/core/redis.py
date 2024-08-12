import redis.asyncio

from . import config


class RedisNotConnectedError(Exception):
    pass


class ConnectionNotAcquiredError(Exception):
    pass


_pool: redis.ConnectionPool | None = None


async def connect(
    url: str = config.redis.url,
    db: int = config.redis.db,
):
    global _pool

    if not _pool:
        _pool = redis.asyncio.ConnectionPool.from_url(url, db=config.redis.db)


async def disconnect():
    global _pool

    if _pool:
        if config.redis.force_rollback:
            conn = redis.asyncio.Redis.from_pool(_pool)
            await conn.flushdb()
            await conn.aclose()

        await _pool.aclose()
        _pool = None


class Session:

    _conn: redis.asyncio.Redis | None = None

    async def __aenter__(self):
        if not _pool:
            raise RedisNotConnectedError

        self._conn = redis.asyncio.Redis.from_pool(_pool)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._conn:
            await self._conn.aclose()
            self._conn = None

    def _check_connection(self):
        if not self._conn:
            raise ConnectionNotAcquiredError

    async def ping(self, *args, **kwargs):
        self._check_connection()
        return await self._conn.ping(*args, **kwargs)

    async def get(self, key: str | bytes, *args, **kwargs):
        self._check_connection()
        return await self._conn.get(key, *args, **kwargs)

    async def set(self, key: str | bytes, *args, **kwargs):
        self._check_connection()
        return await self._conn.set(key, *args, **kwargs)

    async def keys(self, pattern: str | bytes, *args, **kwargs):
        self._check_connection()
        return await self._conn.keys(pattern, *args, **kwargs)

    async def delete(self, key: str | bytes, *args, **kwargs):
        self._check_connection()
        return await self._conn.delete(key, *args, **kwargs)


def session(func):
    async def wrapped_func(*args, **kwargs):
        async with Session() as session_:
            return await func(session_, *args, **kwargs)

    return wrapped_func
