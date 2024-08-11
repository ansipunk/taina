import pytest

import taina.models


@pytest.mark.usefixtures("_redis")
async def test_refresh_token():
    username = "username"
    refresh_token = "refresh"

    saved_token = await taina.models.refresh_token_set(username, refresh_token)
    assert saved_token == refresh_token

    saved_username = await taina.models.refresh_token_get(refresh_token)
    assert saved_username == username

    await taina.models.refresh_token_del(refresh_token)

    with pytest.raises(taina.models.TokenDoesNotExist):
        await taina.models.refresh_token_get(refresh_token)


@pytest.mark.usefixtures("_redis")
async def test_access_token():
    username = "username"
    refresh_token = "refresh"
    access_token = "access"

    saved_token = await taina.models.access_token_set(
        username,
        access_token,
        refresh_token,
    )
    assert saved_token == access_token

    saved_username = await taina.models.access_token_get(access_token)
    assert saved_username == username

    await taina.models.refresh_token_del(refresh_token)

    with pytest.raises(taina.models.TokenDoesNotExist):
        await taina.models.access_token_get(access_token)


@pytest.mark.usefixtures("_redis")
async def test_get_refresh_token_by_access_token():
    username = "username"
    refresh_token = "refresh"
    access_token = "access"

    await taina.models.access_token_set(username, access_token, refresh_token)

    assert await taina.models.refresh_token_get_by_access_token(
        access_token,
    ) == refresh_token


@pytest.mark.usefixtures("_redis")
async def test_get_refresh_token_by_access_token_nonexistent():
    assert await taina.models.refresh_token_get_by_access_token("token") is None
