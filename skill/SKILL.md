---
name: skills-doctor
description: Use only for doctor, skills doctor, skills check, audit skills, scan skill directories, diagnose existing local AI agent skills, or generate a local skills HTML report. Do not use for creating, installing, finding, recommending, or learning to write skills.
---

# Skills Doctor

## Boundary

Use this skill to help the current AI agent inspect local AI agent skills and generate a best-practice HTML report.

Do not modify user skill files. Do not apply patches. Do not install or remove skills. Follow-up fixes are user decisions after reading the report.

## Workflow

1. Confirm the target directories.
   - If the user provides paths, scan those paths.
   - If not, scan only existing common roots such as `.codex/skills`, `.claude/skills`, `~/.codex/skills`, and `~/.claude/skills`.
   - Do not search the entire home directory.

2. Run the deterministic scanner before deep reading any skill bodies:

```bash
python3 -m skills_doctor report --output skills-doctor-report.html
```

3. For explicit paths:

```bash
python3 -m skills_doctor report path/to/skills --output skills-doctor-report.html
```

4. Review the report and summarize the highest-risk findings to the user.

## Loading Model

Use the three-layer model when interpreting the report:

- Index: `name + description`, the trigger surface that may be visible before a skill is selected.
- Load: `SKILL.md`, the content loaded after a skill is selected.
- Runtime: `references/`, `scripts/`, `assets/`, and command output that may be loaded on demand.

Token fields are estimates for relative risk ranking, not billing numbers.

## Review Dimensions

- Structure: `SKILL.md`, frontmatter, name, description, resources.
- Trigger quality: precise positive and negative trigger boundaries.
- Token estimate: Index (`name + description`), Load (`SKILL.md`), Runtime (`references/scripts/assets`).
- Runtime cost: large resources, eager reference loading, and unbounded script output risk.
- Conflicts: overlapping descriptions across skills.
- Safety: dangerous commands, secrets, private endpoints, hardcoded local paths.
- Portability: cross-agent compatibility and local path assumptions.

## Output

Deliver the path to the generated HTML report and a short summary:

- scanned roots and skill count
- P1/P2/P3 finding count
- estimated Index / Load / Runtime token costs
- top risks grouped by Index, Load, and Runtime
- what the user should inspect next
