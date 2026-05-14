# Skills Doctor Report Template

Use this template when producing a manual review or summarizing the generated HTML report.

```markdown
## Skills Doctor Report

### Summary
- Scanned: N roots, N skills
- High risk: N P1, N P2, N P3
- Main pattern: one sentence describing the dominant issue

### Findings
1. [P1/P2/P3] Title
   - Evidence: `path:line` or scanner metric
   - Why it matters: concrete impact
   - Fix: specific rewrite, file move, deletion, or gating rule

### Recommended Changes
- Ordered list of concrete edits by impact.

### Validation
- Commands run and what passed or failed.
- Files inspected manually after the scanner output.
```

## Writing Rules

- Lead with findings, not background.
- Include exact file paths and lines when available.
- Separate scanner facts from agent judgment.
- Redact sensitive values in evidence.
- Do not claim the inspected skills were modified unless the user explicitly asked for edits and they were actually applied.
