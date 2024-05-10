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


def test_get_snippets(client):
    response = client.get("/snippets")
    assert response.status_code == 200
    assert response.json() == []

    # Create a snippet
    client.post("/snippets", json={})

    response = client.get("/snippets")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_snippet(client):
    response = client.get("/snippets/1")
    assert response.status_code == 404

    # Create a snippet
    client.post("/snippets", json={})

    response = client.get("/snippets/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "New Snippet"
    assert response.json()["code"] == ""
    assert response.json()["language"] == ""
