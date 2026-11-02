from flask import Blueprint, jsonify, request

from app.services import loan_service


bp = Blueprint("loans", __name__)


@bp.post("/loans")
def create_loan():
    data = request.get_json(silent=True)
    loan = loan_service.borrow_item(data)
    return jsonify(loan), 201


@bp.put("/loans/<int:loan_id>/return")
def return_loan(loan_id):
    loan = loan_service.return_item(loan_id)
    return jsonify(loan), 200


@bp.get("/loans/student/<student_id>")
def student_loans(student_id):
    return jsonify(loan_service.get_student_loans(student_id)), 200
