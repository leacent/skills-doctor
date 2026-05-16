---
name: skills-doctor
description: Use only for doctor, skills doctor, skills check, audit skills, scan skill directories, diagnose existing local AI agent skills, or generate a local skills health report. Do not use for creating, installing, finding, recommending, or learning to write skills.
---

# Skills Doctor

## Boundary

Use this skill to help the current AI agent inspect local AI agent skills and produce a best-practice health report.

This skill is read-only for inspected user skills. Do not edit, delete, move, install, uninstall, overwrite, or patch any user skill files, including `SKILL.md`, `references/`, `scripts/`, `assets/`, or agent configuration files. Only inspect files, summarize risks, and suggest next edits.

If the user asks to apply fixes, stop this review workflow and ask for explicit confirmation before making any file changes.

## Workflow

1. Confirm the target directories.
   - If the user provides paths, inspect those paths.
   - If not, inspect only existing paths from the known roots list below.
   - Do not search the entire home directory.

1. Build a lightweight inventory before deep reading skill bodies.
   - Find skill directories that contain `SKILL.md`.
   - Record each skill's path, `name`, `description`, approximate size, and resource folders.
   - Prefer file search and directory listing tools over reading every file up front.

1. Read only representative or suspicious files first.
   - Start with `SKILL.md` frontmatter and headings.
   - Inspect `references/`, `scripts/`, or `assets/` only when the issue depends on them.
   - Do not execute scripts from inspected skills unless the user explicitly asks and the command is safe.

1. Apply the review references:
   - Read `references/review-checklist.md` for the full audit rubric.
   - Read `references/anti-patterns.md` when explaining or rewriting a problematic skill.
   - Read `references/report-template.md` before producing a concise chat or Markdown report.
   - Read `references/html-report-template.md` when the user asks for an HTML, visual, shareable, or archiveable report.

1. Summarize the highest-risk findings to the user with exact paths, evidence, impact, and concrete next edits. If generating HTML, write `skills-doctor-report.html` unless the user requests another path.

## Known Skill Roots

Check only paths that exist. This list is intentionally explicit so the agent does not scan the entire home directory.

- Universal: `.agents/skills`, `~/.agents/skills`.
- Project-level: `.codex/skills`, `.claude/skills`, `.cursor/skills`.
- Core global agents: `~/.codex/skills`, `~/.claude/skills`, `~/.cursor/skills`.
- Popular agent-specific roots: `~/.aider-desk/skills`, `~/.augment/skills`, `~/.bob/skills`, `~/.openclaw/skills`, `~/.codeartsdoer/skills`, `~/.codebuddy/skills`, `~/.codemaker/skills`.
- Additional known roots when present: `~/.amp/skills`, `~/.antigravity/skills`, `~/.cline/skills`, `~/.dexto/skills`, `~/.firebender/skills`, `~/.gemini/skills`, `~/.github-copilot/skills`, `~/.kimi/skills`, `~/.opencode/skills`, `~/.warp/skills`.

## Loading Model

Use the three-layer model when interpreting a skill:

- Index: `name + description`, the trigger surface that may be visible before a skill is selected.
- Load: `SKILL.md`, the content loaded after a skill is selected.
- Runtime: `references/`, `scripts/`, `assets/`, and command output that may be loaded on demand.

Token counts are rough estimates for relative risk ranking, not billing numbers.

## Review Dimensions

Use `references/review-checklist.md` as the source of truth for qualitative judgment. Treat deterministic observations, such as file size or repeated trigger terms, as leads rather than proof.

## Output

Deliver either a concise chat/Markdown report or a local HTML report:

- scanned roots and skill count
- P1/P2/P3 finding count
- top risks grouped by Index, Load, and Runtime
- exact paths and evidence for each high-risk issue
- what the user should inspect or change next

For HTML reports, use `references/html-report-template.md`, keep the file self-contained, and tell the user the generated path.
