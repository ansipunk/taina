async def test_user_create(api_client):
    username = "username"
    password = "P@ssw0rd"
    display_name = "Display Name"

    response = await api_client.post(
        "/api/users/",
        json={
            "username": username,
            "password": password,
            "display_name": display_name,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "username": username,
        "display_name": display_name,
    }


async def test_user_create_username_in_use(api_client, user_default):
    response = await api_client.post("/api/users/", json=user_default)
    assert response.status_code == 400


async def test_users_list(api_client, user_default):
    response = await api_client.get("/api/users/")
    assert response.status_code == 200
    assert response.json() == {"users": [{
        "username": user_default["username"],
        "display_name": user_default["display_name"],
    }]}


async def test_users_get(api_client, user_default):
    response = await api_client.get(f"/api/users/{user_default['username']}")
    assert response.status_code == 200
    assert response.json() == {
        "username": user_default["username"],
        "display_name": user_default["display_name"],
    }


async def test_users_get_nonexistent(api_client):
    response = await api_client.get("/api/users/nonexistent")
    assert response.status_code == 404


async def test_users_update(auth_api_client, user_default):
    new_display_name = "New Display Name"

    response = await auth_api_client.put(
        "/api/users/me",
        json={"display_name": new_display_name},
    )

    assert response.status_code == 200
    assert response.json() == {
        "username": user_default["username"],
        "display_name": new_display_name,
    }


async def test_users_update_unauthenticated(api_client):
    response = await api_client.put(
        "/api/users/me",
        json={"display_name": "display name"},
    )

    assert response.status_code == 401


async def test_users_delete(auth_api_client):
    response = await auth_api_client.delete("/api/users/me")
    assert response.status_code == 204

    response = await auth_api_client.get("/api/users/me")
    assert response.status_code == 401


async def test_users_delete_unauthenticated(api_client):
    response = await api_client.delete("/api/users/me")
    assert response.status_code == 401


async def test_users_get_me(auth_api_client, user_default):
    response = await auth_api_client.get("/api/users/me")
    assert response.status_code == 200
    assert response.json() == {
        "username": user_default["username"],
        "display_name": user_default["display_name"],
    }
