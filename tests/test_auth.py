import fastapi
import pytest

import taina.auth


@pytest.mark.usefixtures("_db")
async def test_authenticate_user(user_default, user_default_credentials):
    username, password = user_default_credentials
    user = await taina.auth.authenticate_user(username, password)
    assert user == user_default


@pytest.mark.usefixtures("_db")
async def test_authenticate_nonexistent_user():
    with pytest.raises(taina.auth.AuthenticationError):
        await taina.auth.authenticate_user("nonexistent_username", "password")


@pytest.mark.usefixtures("_db")
async def test_authenticate_user_with_invalid_password(user_default):
    with pytest.raises(taina.auth.AuthenticationError):
        await taina.auth.authenticate_user(user_default["username"], "invalid password")


@pytest.mark.usefixtures("_db")
async def test_get_current_user(user_default):
    token = taina.auth.create_access_token({"sub": user_default["username"]})
    user = await taina.auth.get_current_user(token)
    assert user == user_default


@pytest.mark.usefixtures("_db")
async def test_get_current_user_nonexistent_user():
    token = taina.auth.create_access_token({"sub": "invalid"})

    with pytest.raises(fastapi.HTTPException) as e:
        await taina.auth.get_current_user(token)

    assert e.value.status_code == fastapi.status.HTTP_401_UNAUTHORIZED


@pytest.mark.usefixtures("_db")
async def test_get_current_user_invalid_token():
    with pytest.raises(fastapi.HTTPException) as e:
        await taina.auth.get_current_user("invalid token")

    assert e.value.status_code == fastapi.status.HTTP_401_UNAUTHORIZED


@pytest.mark.usefixtures("_db")
async def test_get_current_user_token_without_username():
    token = taina.auth.create_access_token({})

    with pytest.raises(fastapi.HTTPException) as e:
        await taina.auth.get_current_user(token)

    assert e.value.status_code == fastapi.status.HTTP_401_UNAUTHORIZED
