def test_create_snippets(client):
    response = client.post(
        "/api/snippets",
        json={},
    )
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == ""
    assert response.json()["code"] == ""
    assert response.json()["language"] == ""


def test_get_snippets(client):
    response = client.get("/api/snippets")
    assert response.status_code == 200
    assert response.json() == []

    # Create a snippet
    client.post("/api/snippets", json={})

    response = client.get("/api/snippets")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_snippet(client):
    response = client.get("/api/snippets/1")
    assert response.status_code == 404

    # Create a snippet
    client.post("/api/snippets", json={})

    response = client.get("/api/snippets/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == ""
    assert response.json()["code"] == ""
    assert response.json()["language"] == ""


def test_update_snippet(client):
    post_response = client.post(
        "/api/snippets",
        json={"title": "Initial Title", "language": "python", "code": "print('hello')"},
    )
    snippet_id = post_response.json()["id"]
    assert post_response.status_code == 200
    assert post_response.json()["title"] == "Initial Title"

    update_response = client.put(
        f"/api/snippets/{snippet_id}",
        json={"title": "Updated Title", "code": "print('updated')"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Title"
    assert update_response.json()["code"] == "print('updated')"

    get_response = client.get(f"/api/snippets/{snippet_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Updated Title"
    assert get_response.json()["code"] == "print('updated')"


def test_delete_snippet(client):
    post_response = client.post(
        "/api/snippets",
        json={
            "title": "Delete Test",
            "language": "python",
            "code": "print('delete me')",
        },
    )
    snippet_id = post_response.json()["id"]
    assert post_response.status_code == 200

    delete_response = client.delete(f"/api/snippets/{snippet_id}")
    assert delete_response.status_code == 204  # No Content

    get_response = client.get(f"/api/snippets/{snippet_id}")
    assert get_response.status_code == 404
