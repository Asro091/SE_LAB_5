# Lab 5: Static Code Analysis — Issues Report

The line numbers below refer to the original `address_book.py` supplied for the lab. The four selected issues and fixes are listed below.

| Issue                           | Type / Severity       |                   Original line(s) | Description                                                                                         | Fix Approach                                                                     |
|---------------------------------|-----------------------|-----------------------------------:|-----------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| Unsafe pickle deserialization   | Security / High       |                              60–67 | `pickle.load()` can execute arbitrary code when loading an untrusted backup file.                   | Replaced pickle serialization with JSON and validated the restored contact data. |
| Broad exception handling        | Reliability / Medium  |                              30–36 | `except Exception` catches unrelated errors and can hide programming problems when updating a city. | Check whether the contact exists with `contacts.get()` before updating it.       |
| Non-standard function naming    | Maintainability / Low | 10, 18, 22, 30, 39, 47, 53, 60, 65 | Function names use camelCase instead of Python's usual `snake_case` convention.                     | Renamed functions and updated their call sites.                                  |
| CSV export lacks column headers | Data quality / Low    |                              53–58 | The exported CSV has data rows but does not identify the columns.                                   | Added a header row for Name, Phone, Email, and City.                             |

## Verification

- Pylint: 10.00/10 in the reported final run.
- Bandit: no issues identified in the reported final run.
- Flake8: no output in the reported run, indicating no violations under the enabled checks.
- The demonstration program ran successfully and reported that restored contacts matched the in-memory address book.
