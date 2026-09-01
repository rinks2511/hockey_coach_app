# Contributing to HV Myra Matchday Board

Thank you for contributing! To maintain code quality, maintainability, and security across the repository, please adhere to these guidelines.

---

## 1. Branch Naming Conventions

Use descriptive branch prefixes when creating new branches:
* `feat/feature-name`: New features or enhancements.
* `fix/bug-description`: Bug fixes.
* `docs/documentation-update`: Documentation additions or updates.
* `refactor/component-name`: Code refactoring without behavioral changes.

---

## 2. Commit Message Standards

Follow **Conventional Commits**:
* `feat: add player availability bulk export API`
* `fix: prevent TDZ crash on position token initialization`
* `docs: add ADR for Cloud SQL database migration`

---

## 3. Pull Request Guidelines

1. **Local Verification Required**:
   ```bash
   PYTHONPATH=. pytest backend/tests/
   ```
2. Open Pull Request using the repository [PR Template](.github/PULL_REQUEST_TEMPLATE.md).
3. Ensure all CI automated tests pass before requesting review.
