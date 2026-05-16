# skills-doctor

`skills-doctor` is a local checker and installable skill for AI agent skills. It helps an AI agent inspect local skill directories, identify quality and safety issues, and generate a best-practice HTML report. It supports Python 3.9+.

The scanner does not modify inspected skills, apply patches, or upload local content. The installer only copies the bundled `skills-doctor` skill and its review references into your local agent skills directory.

## What It Checks

- Skill discovery across common local roots such as `.codex/skills`, `.claude/skills`, `.cursor/skills`, `~/.codex/skills`, `~/.claude/skills`, and `~/.cursor/skills`.
- `SKILL.md` structure and frontmatter quality.
- Weak, over-broad, or potentially conflicting trigger descriptions.
- Estimated token cost hotspots across Index, Load, and Runtime layers.
- Progressive disclosure issues.
- Long descriptions, large resources, and high runtime context risk.
- Dangerous command patterns and sensitive values.
- Hardcoded local paths.
- Empty resource directories.
- Agent Review Pack output for qualitative model review after deterministic scanning.

## Install

Install the CLI directly from GitHub with `pipx`, then install the bundled skill:

```bash
pipx install "git+https://github.com/leacent/skills-doctor.git"
skills-doctor install-skill --target all
```

Or use `uv`:

```bash
uv tool install "git+https://github.com/leacent/skills-doctor.git"
skills-doctor install-skill --target all
```

This installs `skills-doctor` into:

- `~/.claude/skills/skills-doctor/SKILL.md`
- `~/.codex/skills/skills-doctor/SKILL.md`
- `~/.cursor/skills/skills-doctor/SKILL.md`

Install only one target if needed:

```bash
skills-doctor install-skill --target claude
```

Existing files are not overwritten unless you pass `--force`. After installation, ask your agent to run `skills doctor`, `audit skills`, or `scan skill directories`.

For local development:

```bash
git clone https://github.com/leacent/skills-doctor.git
cd skills-doctor
python3 -m pip install -e .
```

## Quick Start

Generate an HTML report for the default local roots:

```bash
skills-doctor check
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
skills-doctor check [paths...] --output skills-doctor-report.html
skills-doctor scan [paths...] --format json|markdown|html
skills-doctor report [paths...] --output skills-doctor-report.html
skills-doctor review [paths...] --format markdown|json|html
skills-doctor install-skill --target claude|codex|cursor|all
```

`review` generates an Agent Review Pack with read-only safety rules, scan summary, high-risk files to inspect, and deterministic findings for qualitative model review.

When no path is provided, `skills-doctor` scans existing common roots only. It does not search the whole home directory.

## Report Boundary

The HTML report contains deterministic scan evidence, impact, priority, confidence, and suggested next steps. The installed skill includes prompt-based review references for qualitative judgment. Follow-up actions such as rewriting descriptions, splitting references, moving files, disabling skills, or merging duplicates are left to the user.

## Token Estimate Model

`skills-doctor` reports token cost as estimates, not billing values. The default estimator uses a rough `chars / 4` heuristic for relative risk ranking.

- `estimated_index_tokens`: skill name and description, representing the always-visible trigger surface.
- `estimated_load_tokens`: `SKILL.md`, representing the content loaded after a skill is selected.
- `estimated_runtime_tokens`: references, scripts, and assets, representing potential on-demand context cost.
- `estimated_total_tokens`: the sum of the three estimates.

The HTML report groups findings by Index, Load, and Runtime layers so users can see where context cost and trigger risk come from.

## Skill Form

The installable skill bundle lives under [`skill/`](skill/) and is bundled into the Python package for `install-skill`. `SKILL.md` keeps the workflow short, while `skill/references/` contains the prompt-based review checklist, anti-patterns, and report template. Its trigger is intentionally narrow: use it for `doctor`, `skills check`, `audit skills`, `scan skill directories`, and local skills report requests. Do not use it for creating, installing, finding, or learning how to write skills.

## Development

Run tests:

```bash
python3 -m unittest
```

Run the package directly:

```bash
python3 -m skills_doctor report skill --output /tmp/skills-doctor-report.html
```

## Privacy

`skills-doctor` is local-first. It reads only the directories provided by the user or known local skill roots. Reports redact common secret patterns before display.

## License

MIT
