# Contributing

Thanks for improving `skills-doctor`.

## Project Scope

Keep the project focused on local skills checking and HTML report generation.

In scope:

- Static scanning.
- Deterministic checks.
- Report rendering.
- Agent adapter metadata.
- Tests and documentation.

Out of scope:

- Automatically modifying user skills.
- Applying patches.
- Uploading local skills by default.
- Building a skill marketplace.
- Replacing agent-specific installers.

## Development

```bash
python3 -m unittest
python3 -m skills_doctor report --output /tmp/skills-doctor-report.html
```

Prefer standard library code unless a dependency is clearly necessary.

## Pull Requests

- Keep changes scoped.
- Add or update tests for scanner, analyzer, or report behavior.
- Do not commit real secrets or private endpoints.
- Document new checks in `README.md`.

