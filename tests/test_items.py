def test_get_items_when_database_is_empty(client):
    response = client.get("/items")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == []


def test_create_item_with_valid_data(client):
    response = client.post(
        "/items", json={"name": "Mikroskop", "total_stock": 5}
    )

    assert response.status_code == 201
    item = response.get_json()
    assert item["id"] > 0
    assert item["name"] == "Mikroskop"
    assert item["total_stock"] == 5


def test_create_item_without_name(client):
    response = client.post("/items", json={"total_stock": 5})

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_item_with_negative_stock(client):
    response = client.post(
        "/items", json={"name": "Mikroskop", "total_stock": -1}
    )

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_initial_available_stock_equals_total_stock(client):
    response = client.post(
        "/items", json={"name": "Multimeter", "total_stock": 8}
    )

    item = response.get_json()
    assert item["available_stock"] == item["total_stock"] == 8


def test_get_items_shows_latest_stock(client):
    item = client.post(
        "/items", json={"name": "Mikroskop", "total_stock": 5}
    ).get_json()

    client.post(
        "/loans",
        json={"student_id": "20240001", "item_id": item["id"], "quantity": 2},
    )

    items = client.get("/items").get_json()
    assert items[0]["available_stock"] == 3
