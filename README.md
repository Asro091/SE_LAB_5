# Lab 5: Static Code Analysis — Reflection

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest issues to fix were the inconsistent function naming and missing CSV headers. These required straightforward changes, such as renaming functions to follow Python's `snake_case` convention and adding a header row to the CSV file.

The hardest issue was replacing pickle-based backup and restoration with JSON. This required changing the serialization and deserialization logic and validating the restored data to ensure that the backup remained reliable and secure.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Yes. Bandit flagged `SYNC_PASSWORD = "contacts-demo"` as a possible hardcoded password. However, this was an unused demonstration constant rather than an actual password used for authentication, so the warning was a potential false positive in the context of this program. I removed the unused constant, and Bandit subsequently reported no security issues.

## 3. How would you integrate static analysis tools into your actual software development workflow?

I would integrate Pylint, Flake8, and Bandit into my development workflow and run them regularly while writing code. I would use Pylint to check code quality, Flake8 to identify style violations, and Bandit to detect potential security vulnerabilities. I would also integrate these tools into a CI/CD pipeline so that code is checked automatically before it is merged into the main branch. This would help identify problems early and maintain consistent code quality.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

The code became more readable and maintainable after adopting consistent naming conventions and improving error handling. Adding CSV headers made exported data easier to understand. Replacing pickle with JSON and validating restored contact data improved backup safety. The program continued to run correctly after the changes, and the restored contacts matched the original data. Pylint achieved a score of 10/10, Bandit reported zero issues, and Flake8 produced no output.
