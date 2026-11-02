from app.database import get_db
from app.repositories import item_repository, loan_repository
from app.validators import (
    NotFoundError,
    ValidationError,
    require_non_empty_string,
    require_positive_int,
)


def borrow_item(data):
    if not isinstance(data, dict):
        raise ValidationError("Body JSON tidak valid.")

    student_id = require_non_empty_string(data.get("student_id"), "student_id")
    item_id = require_positive_int(data.get("item_id"), "item_id")
    quantity = require_positive_int(data.get("quantity"), "quantity")

    db = get_db()
    item = item_repository.get_by_id(db, item_id)
    if item is None:
        raise NotFoundError("Item tidak ditemukan.")

    try:
        if not item_repository.decrease_stock(db, item_id, quantity):
            raise ValidationError("Stok tidak mencukupi.")
        loan_id = loan_repository.create(db, student_id, item_id, quantity)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return loan_repository.get_by_id(db, loan_id)


def return_item(loan_id):
    loan_id = require_positive_int(loan_id, "loan_id")

    db = get_db()
    loan = loan_repository.get_by_id(db, loan_id)
    if loan is None:
        raise NotFoundError("Transaksi peminjaman tidak ditemukan.")

    if loan["status"] == "RETURNED":
        raise ValidationError("Transaksi sudah dikembalikan.")

    try:
        loan_repository.update_status(db, loan_id, "RETURNED")
        if not item_repository.increase_stock(
            db, loan["item_id"], loan["quantity"]
        ):
            raise ValidationError("Stok item tidak dapat dipulihkan.")
        db.commit()
    except Exception:
        db.rollback()
        raise

    return loan_repository.get_by_id(db, loan_id)


def get_student_loans(student_id):
    student_id = require_non_empty_string(student_id, "student_id")
    return loan_repository.get_by_student(get_db(), student_id)
