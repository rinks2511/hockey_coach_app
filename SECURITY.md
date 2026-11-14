# Security Policy

## Supported Versions

| Version | Supported          | Status |
| ------- | ------------------ | ------ |
| `main`  | :white_check_mark: | Active production |

---

## Reporting a Vulnerability

We take the security of the **HV Myra Matchday Board Application** seriously. If you discover a security vulnerability, weakness, or accidental credential leak:

1. **Do NOT open a public GitHub issue.**
2. Report the vulnerability privately via **GitHub Security Advisories** or email directly to:
   - **Security Contact:** `singhalrajeev89@gmail.com`
3. Include:
   - Type of vulnerability (e.g. injection, auth bypass, CSRF, secret leak)
   - Affected components, files, or API endpoints
   - Step-by-step reproduction instructions or proof-of-concept
   - Impact assessment

Maintainers will acknowledge receipt within 48 hours and coordinate a patch through a private pull request.

---

## Security Best Practices & Automated Controls

The following automated security controls are enforced across the repository:

1. **Automated Dependency Auditing (`pip-audit` & `npm audit`)**:
   - Every Pull Request runs `pip-audit --strict` against the PyPA and OSV vulnerability databases.
   - Dependencies in `package.json` are maintained with zero known high/critical CVEs.
2. **Static Application Security Testing (`bandit`)**:
   - Python backend code is continuously scanned for common OWASP/CWE vulnerabilities, insecure deserialization, and dangerous standard library calls.
3. **Automated Dependency Scanning (`Dependabot`)**:
   - Weekly automated security updates for Python (`pip`), Node (`npm`), and GitHub Actions.
4. **Secret Leak Prevention**:
   - `.gitignore` rigorously excludes `.env`, `*.key`, `*.pem`, and all credential/service-account files.
   - Developers must never commit hardcoded tokens, API keys, or GCP service account JSON files.
5. **Least-Privilege Infrastructure**:
   - Google Cloud Run operates using a dedicated service account (`hockey-coach-app-sa@hockey-507014.iam.gserviceaccount.com`) strictly scoped to necessary bucket storage and logging roles, avoiding broad Compute Engine Editor permissions.
