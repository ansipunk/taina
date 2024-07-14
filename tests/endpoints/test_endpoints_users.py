async def test_user_create(api_client):
    username = "username"
    password = "password"

    response = await api_client.post(
        "/api/users/",
        json={"username": username, "password": password},
    )

    assert response.status_code == 200
    assert response.json() == {"username": username, "password": password}


async def test_user_create_username_in_use(api_client, user_default):
    response = await api_client.post("/api/users/", json=user_default)
    assert response.status_code == 400


async def test_users_list(api_client, user_default):
    response = await api_client.get("/api/users/")
    assert response.status_code == 200
    assert response.json() == {"users": [user_default]}


async def test_users_get(api_client, user_default):
    response = await api_client.get(f"/api/users/{user_default['username']}")
    assert response.status_code == 200
    assert response.json() == user_default


async def test_users_get_nonexistent(api_client):
    response = await api_client.get("/api/users/nonexistent")
    assert response.status_code == 404


async def test_users_update(api_client, user_default):
    new_password = "new password"

    response = await api_client.put(
        f"/api/users/{user_default['username']}",
        json={"password": new_password},
    )

    assert response.status_code == 200
    assert response.json() == {**user_default, "password": new_password}


async def test_users_update_nonexistent(api_client):
    response = await api_client.put(
        "/api/users/nonexistent",
        json={"password": "password"},
    )

    assert response.status_code == 404


async def test_users_delete(api_client, user_default):
    response = await api_client.delete(f"/api/users/{user_default['username']}")
    assert response.status_code == 204

    response = await api_client.get(f"/api/users/{user_default['username']}")
    assert response.status_code == 404
