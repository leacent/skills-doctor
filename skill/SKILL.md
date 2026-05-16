---
name: skills-doctor
description: Use only for doctor, skills doctor, skills check, audit skills, scan skill directories, diagnose existing local AI agent skills, or generate a local skills HTML report. Do not use for creating, installing, finding, recommending, or learning to write skills.
---

# Skills Doctor

## Boundary

Use this skill to help the current AI agent inspect local AI agent skills and generate a best-practice HTML report.

This skill is read-only for inspected user skills. Do not edit, delete, move, install, uninstall, overwrite, or patch any user skill files, including `SKILL.md`, `references/`, `scripts/`, `assets/`, or agent configuration files. Only generate reports, summaries, and suggested next edits.

If the user asks to apply fixes, stop using this review workflow and ask for explicit confirmation before making any file changes outside generated report output. The `install-skill` command may install or update only the bundled `skills-doctor` skill itself.

## Workflow

1. Confirm the target directories.
   - If the user provides paths, scan those paths.
   - If not, scan only existing common roots such as `.codex/skills`, `.claude/skills`, `.cursor/skills`, `~/.codex/skills`, `~/.claude/skills`, and `~/.cursor/skills`.
   - Do not search the entire home directory.

1. Run the deterministic scanner before deep reading any skill bodies:

```bash
skills-doctor check
```

1. For explicit paths:

```bash
skills-doctor report path/to/skills --output skills-doctor-report.html
```

1. Treat scanner findings as leads, not final judgment. Read only the suspicious or representative `SKILL.md` files first, then inspect `references/`, `scripts/`, or `assets/` when a finding depends on them.

1. Apply the review references:
   - Read `references/review-checklist.md` for the full audit rubric.
   - Read `references/anti-patterns.md` when rewriting or explaining a problematic skill.
   - Read `references/report-template.md` when producing a manual review instead of relying only on the generated HTML report.

1. Summarize the highest-risk findings to the user with exact paths, evidence, impact, and concrete next edits.

## Loading Model

Use the three-layer model when interpreting the report:

- Index: `name + description`, the trigger surface that may be visible before a skill is selected.
- Load: `SKILL.md`, the content loaded after a skill is selected.
- Runtime: `references/`, `scripts/`, `assets/`, and command output that may be loaded on demand.

Token fields are estimates for relative risk ranking, not billing numbers.

## Review Dimensions

Use `references/review-checklist.md` as the source of truth for qualitative judgment. The Python scanner is intentionally limited to deterministic discovery, metrics, and risk signals; the agent should decide whether each signal is actually a problem.

## Output

Deliver the path to the generated HTML report and a short summary:

- scanned roots and skill count
- P1/P2/P3 finding count
- estimated Index / Load / Runtime token costs
- top risks grouped by Index, Load, and Runtime
- what the user should inspect next
