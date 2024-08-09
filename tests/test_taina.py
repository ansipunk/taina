async def test_redirect_to_docs(api_client):
    response = await api_client.get("/", allow_redirects=False)
    assert response.status_code == 307
    assert response.headers["Location"] == "/docs"
