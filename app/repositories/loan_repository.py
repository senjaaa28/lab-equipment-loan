def create(db, student_id, item_id, quantity, status="BORROWED"):
    cursor = db.execute(
        "INSERT INTO loans (student_id, item_id, quantity, status) "
        "VALUES (?, ?, ?, ?)",
        (student_id, item_id, quantity, status),
    )
    return cursor.lastrowid


def get_by_id(db, loan_id):
    row = db.execute(
        "SELECT id, student_id, item_id, quantity, status, created_at "
        "FROM loans WHERE id = ?",
        (loan_id,),
    ).fetchone()
    return dict(row) if row is not None else None


def update_status(db, loan_id, status):
    cursor = db.execute(
        "UPDATE loans SET status = ? WHERE id = ?",
        (status, loan_id),
    )
    return cursor.rowcount == 1


def get_by_student(db, student_id):
    rows = db.execute(
        "SELECT id, student_id, item_id, quantity, status, created_at "
        "FROM loans WHERE student_id = ? ORDER BY id",
        (student_id,),
    ).fetchall()
    return [dict(row) for row in rows]
