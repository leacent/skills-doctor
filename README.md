# skills-doctor

`skills-doctor` is a local checker for AI agent skills. It helps an AI agent inspect local skill directories, identify quality and safety issues, and generate a best-practice HTML report. It supports Python 3.9+.

It does not modify skills, apply patches, install skills, or upload local content.

## What It Checks

- Skill discovery across common local roots such as `.codex/skills`, `.claude/skills`, `~/.codex/skills`, and `~/.claude/skills`.
- `SKILL.md` structure and frontmatter quality.
- Trigger description precision and over-broad descriptions.
- Estimated token cost hotspots across Index, Load, and Runtime layers.
- Progressive disclosure issues.
- Long descriptions, large resources, and high runtime context risk.
- Dangerous command patterns and sensitive values.
- Hardcoded local paths.
- Empty resource directories.
- Potential trigger conflicts between skills.

## Install From Source

```bash
python3 -m pip install -e .
```

## Quick Start

Generate an HTML report for the default local roots:

```bash
skills-doctor report --output skills-doctor-report.html
```

Scan explicit skill roots:

```bash
skills-doctor report ~/.codex/skills ~/.claude/skills --output report.html
```

Print JSON for automation:

```bash
skills-doctor scan ~/.codex/skills --format json
```

Print Markdown for terminal review:

```bash
skills-doctor scan ~/.codex/skills --format markdown
```

## CLI

```bash
skills-doctor scan [paths...] --format json|markdown|html
skills-doctor report [paths...] --output skills-doctor-report.html
skills-doctor review [paths...] --format markdown|json|html
```

When no path is provided, `skills-doctor` scans existing common roots only. It does not search the whole home directory.

## Report Boundary

The HTML report contains evidence, impact, priority, confidence, and suggested next steps. Follow-up actions such as rewriting descriptions, splitting references, moving files, disabling skills, or merging duplicates are left to the user.

## Token Estimate Model

`skills-doctor` reports token cost as estimates, not billing values. The default estimator uses a rough `chars / 4` heuristic for relative risk ranking.

- `estimated_index_tokens`: skill name and description, representing the always-visible trigger surface.
- `estimated_load_tokens`: `SKILL.md`, representing the content loaded after a skill is selected.
- `estimated_runtime_tokens`: references, scripts, and assets, representing potential on-demand context cost.
- `estimated_total_tokens`: the sum of the three estimates.

The HTML report groups findings by Index, Load, and Runtime layers so users can see where context cost and trigger risk come from.

## Skill Form

The installable skill definition lives at [`skill/SKILL.md`](skill/SKILL.md). Its trigger is intentionally narrow: use it for `doctor`, `skills check`, `audit skills`, `scan skill directories`, and local skills report requests. Do not use it for creating, installing, finding, or learning how to write skills.

## Development

Run tests:

```bash
python3 -m unittest
```

Run the package directly:

```bash
python3 -m skills_doctor report tests/fixtures --output /tmp/skills-doctor-report.html
```

## Privacy

`skills-doctor` is local-first. It reads only the directories provided by the user or known local skill roots. Reports redact common secret patterns before display.

## License

MIT
