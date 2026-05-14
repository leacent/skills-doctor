# Security Policy

`skills-doctor` scans local files and may encounter sensitive content in `SKILL.md`, scripts, or references.

## Security Model

- No network access is required.
- No local files are modified by design.
- Reports redact common secret patterns before display.
- The scanner only reads user-provided paths or existing common skill roots.
- The scanner does not search the entire home directory by default.

## Reporting a Vulnerability

Open a private security advisory or email the project maintainers. Include:

- A minimal reproduction.
- Affected version or commit.
- Whether local sensitive data could be exposed.

Do not include real secrets in reports.

