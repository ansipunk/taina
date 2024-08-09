import taina.auth


async def test_obtain_access_token(api_client, user_default, user_default_credentials):
    username, password = user_default_credentials

    response = await api_client.post(
        "/api/tokens/access",
        form={"username": username, "password": password},
    )
    assert response.status_code == 200

    body = response.json()
    assert isinstance(body["access_token"], str)
    assert body["token_type"] == "bearer"

    assert await taina.auth.get_current_user(body["access_token"]) == user_default


async def test_obtain_access_token_authentication_error(api_client, mocker):
    mocker.patch(
        "taina.auth.authenticate_user",
        side_effect=taina.auth.AuthenticationError,
    )

    response = await api_client.post(
        "/api/tokens/access",
        form={"username": "username", "password": "password"},
    )
    assert response.status_code == 401
