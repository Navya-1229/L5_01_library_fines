"""Manage campus library loans, renewals, and overdue fines."""

import ast
import json
import math
import operator
from datetime import datetime
from pathlib import Path

FINE_PER_DAY = 2
DEFAULT_RECORDS_FILE = Path("loans.json")

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

loans = {}


def add_book_loan(student_id, book_id, dates=None):
    """Record a book loan for a student."""
    if not isinstance(student_id, str) or not student_id.strip():
        print("Invalid student ID.")
        return

    if not isinstance(book_id, str) or not book_id.strip():
        print("Invalid book ID.")
        return

    if dates is None:
        dates = []

    dates.append(datetime.now().isoformat(timespec="seconds"))
    loans[student_id] = loans.get(student_id, []) + [book_id]

    print(
        f"{student_id} borrowed {book_id} "
        f"(loan dates on record: {len(dates)})"
    )


def return_book(student_id, book_id):
    """Remove a book from a student's active loans."""
    student_loans = loans.get(student_id)

    if student_loans is None or book_id not in student_loans:
        print(f"No active loan found for {student_id}: {book_id}")
        return

    student_loans.remove(book_id)

    if not student_loans:
        del loans[student_id]


def calculate_fine(days_overdue):
    """Calculate a fine after validating overdue days."""
    if (
        isinstance(days_overdue, bool)
        or not isinstance(days_overdue, int)
    ):
        raise TypeError("Days overdue must be an integer.")

    if days_overdue < 0:
        raise ValueError("Days overdue cannot be negative.")

    return days_overdue * FINE_PER_DAY


def renew_book(student_id, book_id, extra_days):
    """Validate and report a loan renewal."""
    if not isinstance(student_id, str) or not student_id.strip():
        raise ValueError("Student ID cannot be empty.")

    if not isinstance(book_id, str) or not book_id.strip():
        raise ValueError("Book ID cannot be empty.")

    if isinstance(extra_days, bool) or not isinstance(extra_days, int):
        raise TypeError("Renewal days must be an integer.")

    if not 1 <= extra_days <= 14:
        raise ValueError("Renewal period must be between 1 and 14 days.")

    if book_id not in loans.get(student_id, []):
        print(f"No active loan found for {student_id}: {book_id}")
        return

    print(f"Renewed {book_id} for {student_id} by {extra_days} days")


def load_records(file_path=DEFAULT_RECORDS_FILE):
    """Load and validate loan records from a JSON file."""
    path = Path(file_path)

    try:
        with path.open("r", encoding="utf-8") as records_file:
            loaded_records = json.load(records_file)
    except FileNotFoundError:
        loans.clear()
        return
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(
            f"Could not load loan records from {path}: {error}"
        ) from error

    if not isinstance(loaded_records, dict):
        raise ValueError("Loan records must be a JSON object.")

    valid_records = all(
        isinstance(student_id, str)
        and isinstance(book_ids, list)
        and all(isinstance(book_id, str) for book_id in book_ids)
        for student_id, book_ids in loaded_records.items()
    )

    if not valid_records:
        raise ValueError(
            "Loan records contain an invalid student or book entry."
        )

    loans.clear()
    loans.update(loaded_records)


def save_records(file_path=DEFAULT_RECORDS_FILE):
    """Save current loan records as JSON."""
    path = Path(file_path)

    with path.open("w", encoding="utf-8") as records_file:
        json.dump(loans, records_file, indent=2)


def _evaluate_arithmetic(node):
    """Evaluate numeric constants and approved arithmetic operations."""
    if isinstance(node, ast.Expression):
        return _evaluate_arithmetic(node.body)

    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left = _evaluate_arithmetic(node.left)
        right = _evaluate_arithmetic(node.right)

        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("Exponent is too large.")

        result = _ALLOWED_OPERATORS[type(node.op)](left, right)

        if isinstance(result, (int, float)):
            if not math.isfinite(result) or abs(result) > 1_000_000_000:
                raise ValueError("Calculation result is too large.")
        else:
            raise ValueError("Calculation must produce a real number.")

        return result

    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        return _ALLOWED_OPERATORS[type(node.op)](
            _evaluate_arithmetic(node.operand)
        )

    raise ValueError(
        "Rule may contain only numbers and basic arithmetic operators."
    )


def fine_from_rule(rule, days):
    """Calculate a fine using a restricted arithmetic expression."""
    if not isinstance(rule, str) or not rule.strip():
        raise ValueError("Fine rule must be a non-empty string.")

    if isinstance(days, bool) or not isinstance(days, int) or days < 0:
        raise ValueError("Days must be a non-negative integer.")

    expression = rule.replace("days", str(days))

    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate_arithmetic(tree)
    except (SyntaxError, ArithmeticError, TypeError, RecursionError) as error:
        raise ValueError("Invalid fine rule.") from error

    if (
        not isinstance(result, (int, float))
        or not math.isfinite(result)
        or result < 0
    ):
        raise ValueError(
            "Fine rule must produce a finite, non-negative number."
        )

    return result


def print_report():
    """Print all current student loan records."""
    print("Loan Report")

    for student_id, book_ids in sorted(loans.items()):
        print(f"{student_id} -> {book_ids}")


def main():
    """Run the library loan demonstration."""
    add_book_loan("S101", "B-ALGO")
    add_book_loan("S102", "B-NETW")
    add_book_loan("", "B-DBMS")
    add_book_loan("S103", 4521)

    return_book("S999", "B-NONE")
    renew_book("S101", "B-ALGO", 7)

    print("Fine for 5 days:", calculate_fine(5))

    try:
        print("Fine for -3 days:", calculate_fine(-3))
    except ValueError as error:
        print(f"Invalid fine request: {error}")

    print("Fine via rule:", fine_from_rule("days * 2 + 10", 4))

    user_input = input(
        "Days overdue for S102 (press Enter for 0): "
    ).strip()

    try:
        days_overdue = int(user_input or "0")
        print("S102 owes:", calculate_fine(days_overdue))
    except (ValueError, TypeError) as error:
        print(f"Invalid overdue days: {error}")

    save_records()
    load_records()
    print_report()


if __name__ == "__main__":
    main()
