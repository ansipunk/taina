import contextlib

import psycopg
import psycopg.rows
import psycopg_pool
import sqlalchemy
import sqlalchemy.dialects.postgresql
import sqlalchemy.sql.elements

from . import config

metadata = sqlalchemy.MetaData()


class PostgresNotConnectedError(RuntimeError):
    pass


class ConnectionNotAcquiredError(RuntimeError):
    pass


_pool: psycopg_pool.AsyncConnectionPool | None = None
_conn: psycopg.AsyncConnection | None = None
_transaction: psycopg.AsyncTransaction | None = None
_dialect = sqlalchemy.dialects.postgresql.psycopg.PGDialectAsync_psycopg()


async def connect(url: str = config.postgres.url):
    global _pool
    global _conn
    global _transaction

    if config.postgres.force_rollback:
        if not _conn:
            _conn = await psycopg.AsyncConnection.connect(url)

        if not _transaction:
            _transaction = psycopg.AsyncTransaction(_conn, force_rollback=True)

            for _ in _transaction._enter_gen():
                pass
    else:
        if not _pool:
            _pool = psycopg_pool.AsyncConnectionPool(url, open=False)
            await _pool.open()


async def disconnect():
    global _pool
    global _conn
    global _transaction

    if _transaction:
        _transaction._exit_gen(None, None, None)
        _transaction = None

    if _pool:
        await _pool.close()
        _pool = None

    if _conn:
        await _conn.close()
        _conn = None


class Session:

    _conn: psycopg.AsyncConnection | None = None
    _transaction: psycopg.AsyncTransaction | None = None

    async def __aenter__(self):
        if config.postgres.force_rollback:
            if not _conn:
                raise PostgresNotConnectedError

            self._conn = _conn
            return self

        if not _pool:
            raise PostgresNotConnectedError

        self._conn = await _pool.getconn()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._conn and not config.postgres.force_rollback:
            await _pool.putconn(self._conn)

        self._conn = None

    def _compile_query(self, query):
        compiled_query = query.compile(dialect=_dialect)
        return str(compiled_query), compiled_query.params

    @contextlib.asynccontextmanager
    async def transaction(self) -> contextlib.AbstractAsyncContextManager:
        if not self._conn:
            raise ConnectionNotAcquiredError

        async with self._conn.transaction() as transaction:
            self._transaction = transaction
            yield
            self._transaction = None

    @contextlib.asynccontextmanager
    async def _execute(self, query):
        if not self._conn:
            raise ConnectionNotAcquiredError

        str_query, params = self._compile_query(query)

        try:
            async with self._conn.cursor() as cursor:
                await cursor.execute(str_query, params)
                yield cursor
        except Exception:
            if not self._transaction and not _transaction:
                await self._conn.rollback()

            raise
        else:
            if not self._transaction and not _transaction:
                await self._conn.commit()

    async def fetch_one(
        self, query: sqlalchemy.sql.elements.ClauseElement,
    ) -> dict | None:
        async with self._execute(query) as cursor:
            row = await cursor.fetchone()

            if not row:
                return None

            row_factory = psycopg.rows.dict_row(cursor)
            return row_factory(row)

    async def fetch_all(
        self, query: sqlalchemy.sql.elements.ClauseElement,
    ) -> list[dict]:
        async with self._execute(query) as cursor:
            rows = await cursor.fetchall()

            if not rows:
                return []

            row_factory = psycopg.rows.dict_row(cursor)
            return [row_factory(row) for row in rows]

    async def execute(
        self, query: sqlalchemy.sql.elements.ClauseElement,
    ) -> None:
        async with self._execute(query):
            return


def session(func):
    async def wrapped_func(*args, **kwargs):
        async with Session() as session_:
            return await func(session_, *args, **kwargs)

    return wrapped_func
