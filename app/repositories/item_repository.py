def create(db, name, total_stock, available_stock):
    cursor = db.execute(
        "INSERT INTO items (name, total_stock, available_stock) "
        "VALUES (?, ?, ?)",
        (name, total_stock, available_stock),
    )
    return cursor.lastrowid


def get_all(db):
    rows = db.execute(
        "SELECT id, name, total_stock, available_stock FROM items ORDER BY id"
    ).fetchall()
    return [dict(row) for row in rows]


def get_by_id(db, item_id):
    row = db.execute(
        "SELECT id, name, total_stock, available_stock FROM items WHERE id = ?",
        (item_id,),
    ).fetchone()
    return dict(row) if row is not None else None


def decrease_stock(db, item_id, quantity):
    cursor = db.execute(
        "UPDATE items SET available_stock = available_stock - ? "
        "WHERE id = ? AND available_stock >= ?",
        (quantity, item_id, quantity),
    )
    return cursor.rowcount == 1


def increase_stock(db, item_id, quantity):
    cursor = db.execute(
        "UPDATE items SET available_stock = available_stock + ? "
        "WHERE id = ? AND available_stock + ? <= total_stock",
        (quantity, item_id, quantity),
    )
    return cursor.rowcount == 1
