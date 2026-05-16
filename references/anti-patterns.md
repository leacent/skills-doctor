# Skills Doctor Anti-Patterns

Use this reference when explaining or rewriting problematic skills.

## Over-Broad Trigger

Problem:

```yaml
description: Helps with all coding tasks and best practices.
```

Why it is risky: the skill competes with nearly every coding request and gives the agent no clear boundary.

Better:

```yaml
description: Use when reviewing local AI agent skill directories for trigger precision, token cost, progressive disclosure, safety issues, and install-location problems. Do not use for creating or installing new skills.
```

## Body-Only Trigger Rules

Problem: the frontmatter description is generic, while the body explains the actual use case.

Why it is risky: many agents select skills from the frontmatter before reading the body.

Better: put the core trigger and non-use boundary in `description`, then use the body for workflow.

## Eager Reference Loading

Problem:

```md
Read all references before answering.
```

Why it is risky: this burns context even when only one reference is relevant.

Better: list each reference with a narrow condition for reading it.

## Embedded Long Examples

Problem: `SKILL.md` contains long schemas, sample reports, provider matrices, or many code examples.

Why it is risky: the whole body loads after selection, even for simple requests.

Better: move long material into `references/` and summarize the load condition in `SKILL.md`.

## Dangerous Command Normalization

Problem: the skill casually recommends destructive commands such as `rm -rf`, `git reset --hard`, broad `chmod 777`, or install pipes.

Why it is risky: the skill trains the agent to treat high-impact operations as routine.

Better: require explicit user confirmation, explain impact and rollback limits, and prefer reversible alternatives.

## Sensitive Example Values

Problem: examples include real-looking tokens, passwords, private endpoints, or database URLs.

Why it is risky: reports, logs, package registries, or shared conversations may expose secrets.

Better: use placeholders such as `<API_KEY>`, `.env.example`, or environment-variable names.

## Hardcoded Local Path

Problem:

```md
Run `/Users/alice/work/project/scripts/audit.py`.
```

Why it is risky: the skill fails on other machines and agents.

Better:

```md
Run `scripts/audit.py` from the skill directory.
```

## Unbounded Discovery

Problem: the skill tells the agent to scan the entire home directory.

Why it is risky: it is slow, noisy, and may read unrelated private files.

Better: scan only user-provided paths or known skill roots that exist.
