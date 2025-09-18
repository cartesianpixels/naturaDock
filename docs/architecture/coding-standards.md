# Coding Standards

All Python code in this project will adhere strictly to the [PEP 8 -- Style Guide for Python Code](https://peps.python.org/pep-0008/).

Key principles include:
- Max line length of 88 characters.
- Use of Black for automated code formatting.
- Use of Ruff for linting.
- All functions and classes must have clear docstrings.
- Imports should be grouped (standard library, third-party, local application).

## Automation & Enforcement

To ensure consistency and automate quality checks, this project will use `pre-commit` hooks.

- **Configuration:** Formatter (Black) and linter (Ruff) settings will be explicitly defined in the `pyproject.toml` file to ensure all developers use the same standards.
- **Execution:** These hooks will run automatically before each commit, formatting code and checking for linting errors. This prevents non-compliant code from being introduced into the main branch.
