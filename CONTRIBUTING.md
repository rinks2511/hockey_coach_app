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

## 3. Mandatory Pull Request (PR) Policy

> [!IMPORTANT]
> **Direct pushes to the `main` branch are strictly prohibited.**
> All code changes, bug fixes, and documentation updates must be submitted via Pull Requests (PR) from feature branches.

1. **Create Feature Branch**: Never work directly on `main`. Create a feature branch (e.g. `feat/add-teams` or `fix/auth-leak`).
2. **Local Verification Required**:
   ```bash
   PYTHONPATH=. pytest backend/tests/
   ```
3. **Submit PR**: Open a Pull Request targeting `main` using the repository [PR Template](.github/PULL_REQUEST_TEMPLATE.md).
4. **CI Checks**: Ensure all automated GitHub Actions checks pass before merging.
