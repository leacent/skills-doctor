# Skills Doctor Review Checklist

Use this checklist during a read-only review of local AI agent skills. Treat observations as leads, not proof. Read only the files needed to confirm or reject each lead.

## Priority Model

- P1: The skill may fail discovery, leak sensitive data, normalize destructive behavior, or create severe trigger confusion.
- P2: The skill is usable but has meaningful trigger, context, portability, or maintenance risk.
- P3: The issue is low risk, mostly cleanup, or a small clarity improvement.

## Structure

- `SKILL.md` starts with YAML frontmatter delimited by `---`.
- `name` exists, is lowercase hyphenated, portable across agents, and preferably under 64 characters.
- `description` exists and is specific enough to act as the primary trigger surface.
- Resource folders such as `references/`, `scripts/`, and `assets/` are purposeful. Empty folders should be removed.
- Stale metadata files should match the actual skill name, description, and supported agents.

## Trigger Quality

- The frontmatter `description` says what the skill does and when to use it.
- Positive triggers are concrete: user intent, artifact type, domain, or operation.
- Negative boundaries are explicit when adjacent skills could overlap.
- Avoid vague phrases such as "helps with tasks", "best practices", "useful for", "anything", "all tasks", and "common tasks".
- Avoid universal triggers such as "always use", "every request", "use for any", or "all coding tasks" unless the skill is intentionally global.
- Compare nearby skills for trigger overlap. A real conflict exists when two descriptions would reasonably trigger for the same user request without a clear boundary.

## Context And Token Cost

- Keep `SKILL.md` lean and procedural. Around 3,000 words is a practical warning threshold; around 5,000 words is usually too large.
- Move long examples, schemas, provider-specific variants, policies, and reference material into `references/`.
- Do not duplicate the same instructions in `SKILL.md` and references.
- Estimate Index / Load / Runtime token cost roughly for relative risk ranking, not billing.
- Large references or assets are acceptable only when the skill explains when to load them.

## Progressive Disclosure

- `SKILL.md` explains when to read each reference; it should not require loading every reference by default.
- References are named by purpose and are one step away from `SKILL.md`.
- Scripts are used for deterministic repeated operations and have clear CLI usage.
- Script outputs should be bounded or summarized so the agent does not flood context.
- Assets should be loaded only when visual or binary evidence is required.

## Safety And Security

- Skills must not include real credentials, API keys, tokens, private keys, passwords, private endpoints, or sensitive examples.
- Examples should use placeholders and environment variables.
- Dangerous commands such as destructive deletes, broad permission changes, disk formatting, or `curl | sh` must be gated behind explicit user confirmation and safer alternatives.
- Do not instruct the agent to expose secrets, print environment variables, upload local files, or scan an unbounded home directory.
- Reports should redact sensitive evidence before display.

## Portability

- Avoid hardcoded absolute local paths unless clearly marked as local examples.
- Prefer relative paths, `$HOME`, or tool-specific documented locations.
- Keep commands shell-portable where reasonable, and state required tools only when the skill genuinely depends on them.
- Avoid assuming one agent unless the skill is explicitly agent-specific.

## Behavioral Quality

- A good skill gives non-obvious procedure, constraints, decision rules, or reusable tooling.
- A weak skill restates generic agent behavior, adds tutorial padding, or forces expensive work for simple requests.
- The skill should narrow the agent's behavior, not add broad generic policy.
- The recommended fix should be concrete: rewrite description, split references, remove empty folders, gate commands, or redact sensitive values.
