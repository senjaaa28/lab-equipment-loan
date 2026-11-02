import pytest


def create_item(client, name="Mikroskop", total_stock=5):
    response = client.post(
        "/items", json={"name": name, "total_stock": total_stock}
    )
    assert response.status_code == 201
    return response.get_json()


def borrow(client, item_id, quantity, student_id="20240001"):
    return client.post(
        "/loans",
        json={
            "student_id": student_id,
            "item_id": item_id,
            "quantity": quantity,
        },
    )


def get_stock(client, item_id):
    items = client.get("/items").get_json()
    return next(item["available_stock"] for item in items if item["id"] == item_id)


def test_borrow_item_with_valid_data(client):
    item = create_item(client)

    response = borrow(client, item["id"], 2)

    assert response.status_code == 201
    loan = response.get_json()
    assert loan["student_id"] == "20240001"
    assert loan["item_id"] == item["id"]
    assert loan["quantity"] == 2
    assert loan["status"] == "BORROWED"


def test_borrow_item_when_stock_is_sufficient(client):
    item = create_item(client, total_stock=5)

    response = borrow(client, item["id"], 5)

    assert response.status_code == 201
    assert get_stock(client, item["id"]) == 0


def test_borrow_item_when_quantity_exceeds_stock(client):
    item = create_item(client, total_stock=5)

    response = borrow(client, item["id"], 10)

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_borrow_item_with_unknown_item_id(client):
    response = borrow(client, 9999, 1)

    assert response.status_code == 404
    assert "error" in response.get_json()


@pytest.mark.parametrize("quantity", [0, -1])
def test_borrow_item_with_non_positive_quantity(client, quantity):
    item = create_item(client)

    response = borrow(client, item["id"], quantity)

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_stock_decreases_by_borrowed_quantity(client):
    item = create_item(client, total_stock=5)

    borrow(client, item["id"], 2)

    assert get_stock(client, item["id"]) == 3


def test_failed_borrow_does_not_change_stock(client):
    item = create_item(client, total_stock=5)

    response = borrow(client, item["id"], 10)

    assert response.status_code == 400
    assert get_stock(client, item["id"]) == 5
    history = client.get("/loans/student/20240001").get_json()
    assert history == []


def test_return_item_successfully(client):
    item = create_item(client)
    loan = borrow(client, item["id"], 2).get_json()

    response = client.put(f"/loans/{loan['id']}/return")

    assert response.status_code == 200
    assert response.get_json()["status"] == "RETURNED"


def test_return_item_changes_status_to_returned(client):
    item = create_item(client)
    loan = borrow(client, item["id"], 2).get_json()

    returned = client.put(f"/loans/{loan['id']}/return").get_json()

    assert returned["status"] == "RETURNED"


def test_return_item_restores_stock(client):
    item = create_item(client, total_stock=5)
    loan = borrow(client, item["id"], 2).get_json()
    assert get_stock(client, item["id"]) == 3

    client.put(f"/loans/{loan['id']}/return")

    assert get_stock(client, item["id"]) == 5


def test_return_unknown_loan(client):
    response = client.put("/loans/9999/return")

    assert response.status_code == 404
    assert "error" in response.get_json()


def test_return_already_returned_loan(client):
    item = create_item(client)
    loan = borrow(client, item["id"], 2).get_json()
    client.put(f"/loans/{loan['id']}/return")

    response = client.put(f"/loans/{loan['id']}/return")

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_double_return_does_not_increase_stock(client):
    item = create_item(client, total_stock=5)
    loan = borrow(client, item["id"], 2).get_json()
    client.put(f"/loans/{loan['id']}/return")

    client.put(f"/loans/{loan['id']}/return")

    assert get_stock(client, item["id"]) == 5


def test_student_loan_history_with_transactions(client):
    item = create_item(client)
    loan = borrow(client, item["id"], 2).get_json()

    response = client.get("/loans/student/20240001")

    assert response.status_code == 200
    history = response.get_json()
    assert len(history) == 1
    assert history[0]["id"] == loan["id"]
    assert history[0]["student_id"] == "20240001"


def test_student_loan_history_without_transactions(client):
    response = client.get("/loans/student/99999999")

    assert response.status_code == 200
    assert response.get_json() == []


def test_student_loan_history_only_contains_requested_student(client):
    item = create_item(client, total_stock=10)
    borrow(client, item["id"], 1, student_id="20240001")
    borrow(client, item["id"], 2, student_id="20240002")

    history = client.get("/loans/student/20240002").get_json()

    assert len(history) == 1
    assert all(loan["student_id"] == "20240002" for loan in history)
