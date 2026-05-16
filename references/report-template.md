# Skills Doctor Report Template

Use this template when producing a local skills review.

```markdown
## Skills Doctor Report

### Summary
- Scanned: N roots, N skills
- High risk: N P1, N P2, N P3
- Main pattern: one sentence describing the dominant issue

### Findings
1. [P1/P2/P3] Title
   - Evidence: `path:line`, exact snippet, or file metric
   - Why it matters: concrete impact
   - Fix: specific rewrite, file move, deletion, or gating rule

### Recommended Changes
- Ordered list of concrete edits by impact.

### Validation
- Files inspected.
- Commands or searches run, if any.
```

## Writing Rules

- Lead with findings, not background.
- Include exact file paths and lines when available.
- Separate observed facts from agent judgment.
- Redact sensitive values in evidence.
- Do not claim the inspected skills were modified unless the user explicitly asked for edits and they were actually applied.
