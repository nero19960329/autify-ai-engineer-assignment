def test_create_snippets(client):
    response = client.post(
        "/snippets",
        json={},
    )
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "New Snippet"
    assert response.json()["code"] == ""
    assert response.json()["language"] == ""
