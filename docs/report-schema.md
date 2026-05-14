# Report Schema

`skills-doctor` keeps JSON as the structured intermediate format and renders HTML from it.

## Top-Level Fields

- `generated_at`: ISO timestamp.
- `roots`: scanned roots.
- `skills`: discovered skills.
- `findings`: flattened prioritized findings.
- `summary`: aggregate counts.

Token fields are estimates based on a rough `chars / 4` heuristic:

- `estimated_index_tokens`: skill name and description trigger surface.
- `estimated_load_tokens`: `SKILL.md` body loaded after selection.
- `estimated_runtime_tokens`: potential references, scripts, and assets loaded on demand.
- `estimated_total_tokens`: combined estimate.

## Finding

```json
{
  "priority": "P1",
  "category": "trigger",
  "layer": "index",
  "title": "Missing trigger description",
  "path": "/path/to/SKILL.md",
  "line": 1,
  "evidence": "frontmatter.description is missing.",
  "impact": "The description is the primary trigger surface.",
  "recommendation": "Write a concise description that says when to use the skill.",
  "confidence": "high"
}
```

## Priority

- `P1`: high-risk issue, likely to break discovery, safety, or trust.
- `P2`: meaningful quality, portability, conflict, or token-cost issue.
- `P3`: cleanup issue or maintainability signal.

## Layer

- `index`: name, description, trigger metadata, and trigger overlap.
- `load`: `SKILL.md` structure and body loaded after selection.
- `runtime`: references, scripts, assets, command output, secrets, and local path risk.
