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


def test_update_snippet(client):
    post_response = client.post(
        "/snippets",
        json={"title": "Initial Title", "language": "Python", "code": "print('hello')"},
    )
    snippet_id = post_response.json()["id"]
    assert post_response.status_code == 200
    assert post_response.json()["title"] == "Initial Title"

    update_response = client.put(
        f"/snippets/{snippet_id}",
        json={"title": "Updated Title", "code": "print('updated')"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Title"
    assert update_response.json()["code"] == "print('updated')"

    get_response = client.get(f"/snippets/{snippet_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Updated Title"
    assert get_response.json()["code"] == "print('updated')"


def test_delete_snippet(client):
    post_response = client.post(
        "/snippets",
        json={"title": "Delete Test", "language": "Python", "code": "print('delete me')"},
    )
    snippet_id = post_response.json()["id"]
    assert post_response.status_code == 200

    delete_response = client.delete(f"/snippets/{snippet_id}")
    assert delete_response.status_code == 204  # No Content

    get_response = client.get(f"/snippets/{snippet_id}")
    assert get_response.status_code == 404
