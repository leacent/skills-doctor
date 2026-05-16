# Contributing

Thanks for improving `skills-doctor`.

## Project Scope

Keep the project focused on read-only local skills review guidance for AI agents.

In scope:

- Clear review workflows in `SKILL.md`.
- Practical audit rubrics in `references/review-checklist.md`.
- Concrete anti-patterns and safer alternatives.
- Report templates that help agents produce concise findings.
- Documentation that helps users install the skill with `npx skills`.

Out of scope:

- Automatically modifying user skills.
- Applying patches.
- Uploading local skills by default.
- Adding a custom installer or package manager.
- Reintroducing a bundled CLI or background service.
- Building a skill marketplace.

## Development

```bash
npx skills add . --list
```

Prefer plain Markdown and keep the skill easy to inspect.

## Pull Requests

- Keep changes scoped.
- Keep `SKILL.md` short and procedural.
- Move long examples or rubrics into `references/`.
- Do not commit real secrets or private endpoints.
- Document new review dimensions in `README.md`.
