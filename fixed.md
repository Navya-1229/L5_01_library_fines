# Static Code Analysis — Fixes



| No. | Issue | Tool / Type | Fix Applied |
|---:|---|---|---|
| 1 | Unsafe use of `eval()` | Bandit B307 — Security | Replaced `eval()` with a restricted arithmetic evaluator using Python's `ast` module and allowed operators. |
| 2 | Bare exception handling | Pylint W0702, Flake8 E722 — Reliability | Replaced bare `except` clauses with specific exception types to improve error handling. |
| 3 | Mutable default argument (`dates=[]`) | Pylint W0102 — Reliability | Changed the default argument to `dates=None` and initialized a new list inside the function. |
| 4 | Negative overdue days | Logic error — Validation | Added validation to reject negative overdue days and prevent invalid fine calculations. |
| 5 | Unused import (`os`) | Pylint W0611, Flake8 F401 — Code quality | Removed the unused import. |
| 6 | Missing file encoding | Pylint W1514 — Portability | Added `encoding="utf-8"` when opening files. |
| 7 | Unsafe file handling | Pylint R1732 — Reliability | Used `with` statements to ensure files are closed properly. |
| 8 | Incorrect function naming (`renewBook`) | Pylint C0103 — Style | Renamed the function to `renew_book()` to follow Python naming conventions. |
| 9 | Missing module and function docstrings | Pylint C0114, C0116 — Maintainability | Added docstrings to describe the module and functions. |
| 10 | Excessive line length and spacing errors | Flake8 E501, E302, E305 — Style | Wrapped long statements and corrected blank-line spacing. |
| 11 | Use of a global statement | Pylint W0603 — Maintainability | Updated the existing `loans` dictionary with `clear()` and `update()` instead of reassigning it. |
| 12 | Invalid identifiers and renewal periods | Input validation — Reliability | Added checks for student IDs, book IDs, and renewal durations before updating records. |
