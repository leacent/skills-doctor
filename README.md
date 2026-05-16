# skills-doctor

[English](README.md) | [简体中文](README.zh-CN.md)

`skills-doctor` is an Agent Skill for auditing local AI agent skills. It guides an AI agent through a read-only review of local skill directories, trigger quality, context cost, progressive disclosure, safety risks, and maintainability issues.

It is intentionally just a skill: no Python package, no background service, and no automatic file edits.

## Install

Install with the open Agent Skills CLI:

```bash
npx skills add leacent/skills-doctor -g
```

Then ask your agent:

```text
Use skills-doctor to audit my local agent skills.
```

The `-g` flag installs globally so compatible agents can use the skill across projects.

## What It Checks

- Skill discovery across universal, project-level, and popular agent-specific roots, including `.agents/skills`, `~/.agents/skills`, Claude Code, Codex, Cursor, OpenClaw, Cline, Gemini CLI, OpenCode, Warp, Augment, CodeBuddy, and other known skill directories when they exist.
- `SKILL.md` structure and frontmatter quality.
- Weak, over-broad, or potentially conflicting trigger descriptions.
- Index / Load / Runtime context cost using rough relative estimates.
- Progressive disclosure problems, such as eager reference loading.
- Large `SKILL.md` bodies, large references, and runtime context risk.
- Dangerous command patterns and sensitive example values.
- Hardcoded local paths and portability issues.
- Empty or stale resource directories.

## Repository Layout

```text
skills-doctor/
├── SKILL.md
├── references/
│   ├── anti-patterns.md
│   ├── report-template.md
│   └── review-checklist.md
├── README.md
├── README.zh-CN.md
└── LICENSE
```

## Review Boundary

`skills-doctor` is read-only by default. It tells the agent not to edit, delete, move, install, uninstall, overwrite, or patch inspected user skills. It should only inspect files, summarize risks, and suggest next edits.

If the user asks the agent to apply fixes, that is a separate task and should require explicit confirmation.

## Review Model

The skill uses a three-layer model:

- `Index`: `name + description`, the trigger surface visible before selection.
- `Load`: `SKILL.md`, the body loaded after a skill is selected.
- `Runtime`: `references/`, `scripts/`, `assets/`, and command output loaded on demand.

Token counts are rough estimates for relative risk ranking, not billing values.

## Default Skill Roots

When the user does not provide paths, `skills-doctor` asks the agent to inspect only known roots that already exist:

- Universal: `.agents/skills`, `~/.agents/skills`.
- Project-level: `.codex/skills`, `.claude/skills`, `.cursor/skills`.
- Core global agents: `~/.codex/skills`, `~/.claude/skills`, `~/.cursor/skills`.
- Popular agent-specific roots: `~/.aider-desk/skills`, `~/.augment/skills`, `~/.bob/skills`, `~/.openclaw/skills`, `~/.codeartsdoer/skills`, `~/.codebuddy/skills`, `~/.codemaker/skills`.
- Additional known roots when present: `~/.amp/skills`, `~/.antigravity/skills`, `~/.cline/skills`, `~/.dexto/skills`, `~/.firebender/skills`, `~/.gemini/skills`, `~/.github-copilot/skills`, `~/.kimi/skills`, `~/.opencode/skills`, `~/.warp/skills`.

It should not search the entire home directory.

## References

- `references/review-checklist.md`: the full audit rubric.
- `references/anti-patterns.md`: examples of common skill design problems and better alternatives.
- `references/report-template.md`: a compact report format for the final response.

## Privacy

`skills-doctor` is local-first. It instructs the agent to inspect only user-provided paths or known local skill roots, avoid unbounded home-directory scans, and redact sensitive values in reports.

## License

MIT
