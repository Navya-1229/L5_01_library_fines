# Static Code Analysis — Issues

| Issue | Type | Line(s) in Original Code | Description | Fix Approach |
|---|---|---|---|---|
| Unsafe use of `eval()` | Security — Medium | 45 | Bandit B307 reports that `eval()` may execute unsafe expressions. | Replace it with a restricted arithmetic evaluator. |
| Bare exception handling | Reliability — Medium | 21–22 | Bandit B110 and Pylint W0702 flag the bare exception and ignored error. | Check whether the loan and book exist before removing them. |
| Mutable default argument | Bug | 9 | Pylint W0102 reports that `dates=[]` is a dangerous default. The same list is reused between calls. | Use `None` as the default and initialize a new list inside the function. |
| Negative overdue days | Logic bug | 24, 62 | Negative days produce a negative fine. | Reject negative values with `ValueError`. |
| Unsafe user input conversion | Reliability | 62 | Invalid text passed to `int()` can crash the program. | Validate input and handle `ValueError`. |
| Unsafe file handling | Reliability | 34–41 | Files are opened without context managers or explicit encoding. | Use `with open(...)` and specify UTF-8 encoding. |
| Unused import | Style | 2 | Pylint W0611 and Flake8 F401 report the unused `os` import. | Remove the import. |
| Missing docstrings | Maintainability | 1, 9, 16, 24, 27, 33, 39, 44, 47, 52 | Pylint reports missing module and function documentation. | Add module and function docstrings. |
| Incorrect function naming | Style | 27 | Pylint C0103 flags `renewBook` for not following snake_case. | Rename it to `renew_book`. |
| Poor string formatting | Style | 14, 31 | Pylint C0209 and Flake8 E501 identify formatting and line-length issues. | Use f-strings and wrap long lines. |
| Global fine-rate modification | Logic/design | 27–29 | Renewal changes the fine rate for all subsequent calculations. | Keep the rate fixed and validate the renewal period. |

## Original Pylint score

**6.07/10**


