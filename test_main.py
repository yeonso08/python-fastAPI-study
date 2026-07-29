# --- Category ---

def test_category_post(client):
    response = client.post("/categories/", json={"name": "전자기기"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "전자기기"
    assert "id" in data


def test_category_get_list(client, category_id):
    response = client.get("/categories/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_category_put(client, category_id):
    response = client.put(f"/categories/{category_id}", json={"name": "가전"})
    assert response.status_code == 200
    assert response.json()["name"] == "가전"


def test_category_put_404(client):
    response = client.put("/categories/9999", json={"name": "가전"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


def test_category_delete(client, category_id):
    response = client.delete(f"/categories/{category_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Category deleted"}


def test_category_delete_404(client):
    response = client.delete("/categories/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


# --- Item ---

def test_item_post(client, category_id):
    response = client.post("/items/", json={
        "name": "Foo",
        "price": 5000,
        "is_available": True,
        "category_id": category_id,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Foo"
    assert data["price"] == 5000
    assert data["category_id"] == category_id


def test_item_get_list(client, item):
    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_item_get_by_id(client, item):
    response = client.get(f"/items/{item['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Foo"


def test_item_get_404(client):
    response = client.get("/items/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_item_put(client, item, category_id):
    response = client.put(f"/items/{item['id']}", json={
        "name": "Bar",
        "price": 9000,
        "is_available": False,
        "category_id": category_id,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Bar"
    assert data["price"] == 9000
    assert data["is_available"] is False


def test_item_put_404(client, category_id):
    response = client.put("/items/9999", json={
        "name": "Bar",
        "price": 9000,
        "is_available": False,
        "category_id": category_id,
    })
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_item_delete(client, item):
    response = client.delete(f"/items/{item['id']}")
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted"}

    # 삭제 후엔 다시 조회하면 404여야 함
    get_response = client.get(f"/items/{item['id']}")
    assert get_response.status_code == 404


def test_item_delete_404(client):
    response = client.delete("/items/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
