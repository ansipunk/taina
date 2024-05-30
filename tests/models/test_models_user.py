import pytest

import taina.models


@pytest.mark.usefixtures("_db")
async def test_user_create():
    username = "username"
    password = "password"

    user = await taina.models.user_create(username, password)

    assert user["username"] == username
    assert user["password"] == password


async def test_user_create_username_in_use(user_default):
    with pytest.raises(taina.models.UsernameInUse):
        await taina.models.user_create(user_default["username"], "password")


async def test_user_get(user_default):
    user = await taina.models.user_get(user_default["username"])
    assert user["username"] == user_default["username"]
    assert user["password"] == user_default["password"]


@pytest.mark.usefixtures("_db")
async def test_user_get_nonexistent():
    with pytest.raises(taina.models.UserDoesNotExist):
        await taina.models.user_get("nonexistent")


async def test_user_list(user_default, user):
    user_a = user_default
    user_b = await user()
    users = await taina.models.user_list()
    assert users == [user_a, user_b]


async def test_user_update(user_default):
    new_password = "new password"
    user = await taina.models.user_update(user_default["username"], new_password)
    assert user["username"] == user_default["username"]
    assert user["password"] == new_password


@pytest.mark.usefixtures("_db")
async def test_user_update_nonexistent():
    with pytest.raises(taina.models.UserDoesNotExist):
        await taina.models.user_update("nonexistent", "password")


async def test_user_delete(user_default):
    await taina.models.user_delete(user_default["username"])

    with pytest.raises(taina.models.UserDoesNotExist):
        await taina.models.user_get(user_default["username"])
