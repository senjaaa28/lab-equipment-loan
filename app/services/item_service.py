from app.database import get_db
from app.repositories import item_repository
from app.validators import (
    ValidationError,
    require_non_empty_string,
    require_non_negative_int,
)


def list_items():
    return item_repository.get_all(get_db())


def add_item(data):
    if not isinstance(data, dict):
        raise ValidationError("Body JSON tidak valid.")

    name = require_non_empty_string(data.get("name"), "name")
    total_stock = require_non_negative_int(
        data.get("total_stock"), "total_stock"
    )

    db = get_db()
    try:
        item_id = item_repository.create(db, name, total_stock, total_stock)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return item_repository.get_by_id(db, item_id)
