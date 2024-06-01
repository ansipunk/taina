import pytest

import taina.models
import taina.schemas


@pytest.mark.usefixtures("_db")
async def test_user_create():
    schema = taina.schemas.UserCreate(
        username="username",
        password="password",
    )

    user = await taina.models.user_create(schema)

    assert user["username"] == schema.username
    assert user["password"] == schema.password


async def test_user_create_username_in_use(user_default):
    with pytest.raises(taina.models.UsernameInUse):
        await taina.models.user_create(
            taina.schemas.UserCreate(
                username=user_default["username"],
                password="password",
            ),
        )


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
    schema = taina.schemas.UserUpdate(password="new password")
    user = await taina.models.user_update(user_default["username"], schema)
    assert user["username"] == user_default["username"]
    assert user["password"] == schema.password


@pytest.mark.usefixtures("_db")
async def test_user_update_nonexistent():
    with pytest.raises(taina.models.UserDoesNotExist):
        await taina.models.user_update(
            "nonexistent",
            taina.schemas.UserUpdate(password="password"),
        )


async def test_user_delete(user_default):
    await taina.models.user_delete(user_default["username"])

    with pytest.raises(taina.models.UserDoesNotExist):
        await taina.models.user_get(user_default["username"])
