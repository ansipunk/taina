import taina.auth


async def test_obtain_access_token(api_client, user_default, user_default_credentials):
    username, password = user_default_credentials

    response = await api_client.post(
        "/api/tokens/obtain",
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
        "/api/tokens/obtain",
        form={"username": "username", "password": "password"},
    )
    assert response.status_code == 401


async def test_refresh_token(api_client, user_default, user_default_credentials):
    username, password = user_default_credentials

    response = await api_client.post(
        "/api/tokens/obtain",
        form={"username": username, "password": password},
    )
    assert response.status_code == 200

    body = response.json()
    refresh_token = body["refresh_token"]

    response = await api_client.post(
        "/api/tokens/refresh",
        query_string={"grant_type": "refresh", "refresh_token": refresh_token},
    )
    assert response.status_code == 200

    body = response.json()
    refresh_token = body["refresh_token"]
    access_token = body["access_token"]

    response = await api_client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    response = await api_client.post(
        "/api/tokens/refresh",
        query_string={"grant_type": "refresh", "refresh_token": refresh_token},
    )
    assert response.status_code == 200


async def test_refresh_token_invalid_token(api_client):
    response = await api_client.post(
        "/api/tokens/refresh",
        query_string={"grant_type": "refresh", "refresh_token": "invalid token"},
    )
    assert response.status_code == 401


async def test_revoke_token_with_access_token(
    api_client, user_default, user_default_credentials,
):
    username, password = user_default_credentials

    response = await api_client.post(
        "/api/tokens/obtain",
        form={"username": username, "password": password},
    )
    assert response.status_code == 200

    body = response.json()
    access_token = body["access_token"]
    refresh_token = body["refresh_token"]

    response = await api_client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    response = await api_client.post(
        "/api/tokens/revoke",
        query_string={"access_token": access_token},
    )
    assert response.status_code == 200

    response = await api_client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 401

    response = await api_client.post(
        "/api/tokens/refresh",
        query_string={"grant_type": "refresh", "refresh_token": refresh_token},
    )
    assert response.status_code == 401


async def test_revoke_token_with_refresh_token(
    api_client, user_default, user_default_credentials,
):
    username, password = user_default_credentials

    response = await api_client.post(
        "/api/tokens/obtain",
        form={"username": username, "password": password},
    )
    assert response.status_code == 200

    body = response.json()
    access_token = body["access_token"]
    refresh_token = body["refresh_token"]

    response = await api_client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    response = await api_client.post(
        "/api/tokens/revoke",
        query_string={"refresh_token": refresh_token},
    )
    assert response.status_code == 200

    response = await api_client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 401

    response = await api_client.post(
        "/api/tokens/refresh",
        query_string={"grant_type": "refresh", "refresh_token": refresh_token},
    )
    assert response.status_code == 401


async def test_revoke_token_without_access_token_or_refresh_token(api_client):
    response = await api_client.post("/api/tokens/revoke")
    assert response.status_code == 400
