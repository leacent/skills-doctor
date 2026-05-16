# Skills Doctor HTML Report Template

Use this template when the user asks for a shareable, archiveable, or visual local skills health report.

## Output File

Prefer `skills-doctor-report.html` unless the user requests another path.

## HTML Template

Replace bracketed placeholders with the actual review results. Keep the report self-contained: inline CSS, no remote scripts, and no external assets.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Skills Doctor Report</title>
  <style>
    :root {
      --bg: #f7f8fb;
      --panel: #ffffff;
      --ink: #172033;
      --muted: #667085;
      --line: #d9e0ea;
      --p1: #b42318;
      --p2: #b54708;
      --p3: #475467;
      --ok: #027a48;
      --accent: #175cd3;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font: 14px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    header {
      background: linear-gradient(135deg, #101828, #1d2939);
      color: #fff;
      padding: 36px 28px;
    }
    header p { color: #d0d5dd; max-width: 760px; }
    main { max-width: 1160px; margin: 0 auto; padding: 24px; }
    h1, h2, h3 { margin: 0; }
    h2 { font-size: 18px; margin-bottom: 12px; }
    h3 { font-size: 15px; margin-bottom: 8px; }
    .grid { display: grid; gap: 16px; }
    .metrics { grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); }
    .split { grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }
    .card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 16px;
      box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
    }
    .metric-value { font-size: 28px; font-weight: 700; }
    .metric-label, .muted { color: var(--muted); }
    .section { margin-top: 22px; }
    .badge {
      display: inline-block;
      min-width: 34px;
      border-radius: 999px;
      padding: 2px 8px;
      color: #fff;
      font-size: 12px;
      font-weight: 700;
      text-align: center;
    }
    .p1 { background: var(--p1); }
    .p2 { background: var(--p2); }
    .p3 { background: var(--p3); }
    .ok { background: var(--ok); }
    details {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 10px;
      margin-bottom: 10px;
      overflow: hidden;
    }
    summary {
      cursor: pointer;
      display: grid;
      grid-template-columns: auto 1fr auto;
      gap: 12px;
      align-items: center;
      padding: 14px 16px;
      list-style: none;
    }
    summary::-webkit-details-marker { display: none; }
    .detail-body {
      border-top: 1px solid var(--line);
      padding: 14px 16px;
      display: grid;
      grid-template-columns: 140px 1fr;
      gap: 8px 12px;
    }
    code {
      background: #f2f4f7;
      border: 1px solid #eaecf0;
      border-radius: 5px;
      padding: 1px 5px;
      word-break: break-word;
    }
    table { width: 100%; border-collapse: collapse; }
    th, td {
      border-bottom: 1px solid var(--line);
      padding: 10px;
      text-align: left;
      vertical-align: top;
    }
    th { color: var(--muted); font-weight: 600; }
    footer { color: var(--muted); text-align: center; padding: 26px; }
    @media (max-width: 720px) {
      main { padding: 16px; }
      summary { grid-template-columns: 1fr; }
      .detail-body { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <header>
    <h1>Skills Doctor Report</h1>
    <p>[One-sentence health summary. Mention that inspected skills were not modified.]</p>
  </header>

  <main>
    <section class="grid metrics">
      <div class="card"><div class="metric-value">[N]</div><div class="metric-label">Roots scanned</div></div>
      <div class="card"><div class="metric-value">[N]</div><div class="metric-label">Skills found</div></div>
      <div class="card"><div class="metric-value">[N]</div><div class="metric-label">Findings</div></div>
      <div class="card"><div class="metric-value">[P1/P2/P3]</div><div class="metric-label">Risk split</div></div>
    </section>

    <section class="section grid split">
      <div class="card">
        <h2>Index Layer</h2>
        <p class="muted">Name and description trigger surface.</p>
        <p>[Top trigger risks, weak descriptions, or conflicts.]</p>
      </div>
      <div class="card">
        <h2>Load Layer</h2>
        <p class="muted">SKILL.md content loaded after selection.</p>
        <p>[Large bodies, unclear workflow, duplicated instructions.]</p>
      </div>
      <div class="card">
        <h2>Runtime Layer</h2>
        <p class="muted">References, scripts, assets, and command output.</p>
        <p>[Large references, unsafe scripts, secret exposure risk.]</p>
      </div>
    </section>

    <section class="section">
      <h2>Findings</h2>
      <details open>
        <summary>
          <span class="badge p1">P1</span>
          <strong>[Finding title]</strong>
          <span class="muted">[category] · [confidence]</span>
        </summary>
        <div class="detail-body">
          <div class="muted">Location</div><div><code>[path:line]</code></div>
          <div class="muted">Evidence</div><div>[redacted evidence]</div>
          <div class="muted">Impact</div><div>[why this matters]</div>
          <div class="muted">Suggested next edit</div><div>[specific user-approved fix]</div>
        </div>
      </details>
    </section>

    <section class="section card">
      <h2>Skill Inventory</h2>
      <table>
        <thead>
          <tr><th>Skill</th><th>Path</th><th>Trigger summary</th><th>Status</th></tr>
        </thead>
        <tbody>
          <tr><td>[name]</td><td><code>[path]</code></td><td>[description summary]</td><td><span class="badge ok">OK</span></td></tr>
        </tbody>
      </table>
    </section>

    <section class="section card">
      <h2>Next Steps</h2>
      <ol>
        <li>[Highest-impact user-approved edit.]</li>
        <li>[Second edit.]</li>
        <li>[Validation step.]</li>
      </ol>
    </section>
  </main>

  <footer>Generated by skills-doctor. Keep reports local if they include private paths or project details.</footer>
</body>
</html>
```

## Rules

- Redact secrets and private values before writing the report.
- Do not embed full private skill bodies unless the user explicitly asks.
- Do not claim files were changed unless edits were separately requested and actually applied.
- Prefer concise evidence over long excerpts.
