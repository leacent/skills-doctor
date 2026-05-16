from __future__ import annotations

import html
import json
from dataclasses import asdict
from pathlib import Path

from .models import Finding, ScanResult, SkillRecord


def render_result(result: ScanResult, output_format: str) -> str:
    if output_format == "json":
        return render_json(result)
    if output_format == "markdown":
        return render_markdown(result)
    if output_format == "html":
        return render_html(result)
    raise ValueError(f"unsupported format: {output_format}")


def render_json(result: ScanResult) -> str:
    return json.dumps(asdict(result), ensure_ascii=False, indent=2)


def render_review_pack(result: ScanResult, output_format: str) -> str:
    if output_format == "json":
        payload = {
            "scan": asdict(result),
            "agent_review": _review_pack_data(result),
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)
    if output_format == "markdown":
        return render_review_markdown(result)
    if output_format == "html":
        return render_review_html(result)
    raise ValueError(f"unsupported format: {output_format}")


def render_review_markdown(result: ScanResult) -> str:
    lines = [
        "# Skills Doctor Agent Review Pack",
        "",
        "Use this pack to guide an AI agent's qualitative review after deterministic scanning.",
        "",
        "## Safety Boundary",
        "",
        "- Treat this review as read-only.",
        "- Do not edit, delete, move, install, uninstall, overwrite, or patch user skill files.",
        "- Only inspect files, summarize findings, and propose concrete next edits for the user to approve separately.",
        "",
        "## Scan Summary",
        "",
        f"- Generated: `{result.generated_at}`",
        f"- Roots: `{result.summary.get('roots', 0)}`",
        f"- Skills: `{result.summary.get('skills', 0)}`",
        f"- Findings: `{result.summary.get('findings', 0)}`",
        f"- P1/P2/P3: `{result.summary.get('p1', 0)}` / `{result.summary.get('p2', 0)}` / `{result.summary.get('p3', 0)}`",
        f"- Estimated Index / Load / Runtime tokens: `{result.summary.get('estimated_index_tokens', 0)}` / `{result.summary.get('estimated_load_tokens', 0)}` / `{result.summary.get('estimated_runtime_tokens', 0)}`",
        "",
        "## Review Procedure",
        "",
        "1. Start with P1 findings, then P2 trigger and conflict findings.",
        "2. Read only the suspicious or representative `SKILL.md` files first.",
        "3. Inspect `references/`, `scripts/`, or `assets/` only when a finding depends on them.",
        "4. Confirm whether each scanner signal is a real issue or an acceptable trade-off.",
        "5. Return exact paths, evidence, impact, and suggested next edits. Do not apply changes.",
        "",
        "## High-Risk Files To Inspect",
        "",
    ]
    review_data = _review_pack_data(result)
    if review_data["files_to_inspect"]:
        for item in review_data["files_to_inspect"]:
            lines.append(f"- `{item}`")
    else:
        lines.append("- No high-risk files detected.")

    lines.extend([
        "",
        "## Deterministic Findings",
        "",
    ])
    if not result.findings:
        lines.append("No findings detected.")
    for index, finding in enumerate(result.findings, start=1):
        location = finding.path if finding.line is None else f"{finding.path}:{finding.line}"
        lines.extend([
            f"{index}. **[{finding.priority}] {finding.title}**",
            f"   - Category: `{finding.category}`",
            f"   - Layer: `{finding.layer}`",
            f"   - Location: `{location}`",
            f"   - Evidence: `{_redact_for_display(finding.evidence)}`",
            f"   - Impact: {finding.impact}",
            f"   - Suggested next edit: {finding.recommendation}",
            "",
        ])
    return "\n".join(lines)


def render_review_html(result: ScanResult) -> str:
    review = f"""
    <section class="section card">
      <h2>Agent Review Pack</h2>
      <p class="muted">Use this section to guide qualitative AI review after deterministic scanning.</p>
      <h3>Safety Boundary</h3>
      <ul>
        <li>Treat this review as read-only.</li>
        <li>Do not edit, delete, move, install, uninstall, overwrite, or patch user skill files.</li>
        <li>Only inspect files, summarize findings, and propose concrete next edits for separate user approval.</li>
      </ul>
      <h3>Review Procedure</h3>
      <ol>
        <li>Start with P1 findings, then P2 trigger and conflict findings.</li>
        <li>Read only suspicious or representative SKILL.md files first.</li>
        <li>Inspect references, scripts, or assets only when a finding depends on them.</li>
        <li>Confirm whether each scanner signal is a real issue or an acceptable trade-off.</li>
        <li>Return exact paths, evidence, impact, and suggested next edits. Do not apply changes.</li>
      </ol>
      <h3>High-Risk Files To Inspect</h3>
      {_review_files_html(_review_pack_data(result)["files_to_inspect"])}
    </section>
"""
    return render_html(result).replace("  <footer>", f"{review}\n  <footer>")


def render_markdown(result: ScanResult) -> str:
    lines = [
        "# Skills Doctor Report",
        "",
        "## Summary",
        "",
        f"- Generated: `{result.generated_at}`",
        f"- Roots: `{result.summary.get('roots', 0)}`",
        f"- Skills: `{result.summary.get('skills', 0)}`",
        f"- Findings: `{result.summary.get('findings', 0)}`",
        f"- P1/P2/P3: `{result.summary.get('p1', 0)}` / `{result.summary.get('p2', 0)}` / `{result.summary.get('p3', 0)}`",
        f"- Estimated total tokens: `{result.summary.get('estimated_total_tokens', 0)}`",
        f"- Estimated index tokens: `{result.summary.get('estimated_index_tokens', 0)}`",
        f"- Estimated load tokens: `{result.summary.get('estimated_load_tokens', 0)}`",
        f"- Estimated runtime tokens: `{result.summary.get('estimated_runtime_tokens', 0)}`",
        "",
        "Token estimates use a rough `chars / 4` heuristic for relative risk ranking, not billing.",
        "",
        "## Findings",
        "",
    ]

    if not result.findings:
        lines.append("No findings detected.")
    for index, finding in enumerate(result.findings, start=1):
        location = finding.path if finding.line is None else f"{finding.path}:{finding.line}"
        lines.extend([
            f"{index}. **[{finding.priority}] {finding.title}**",
            f"   - Category: `{finding.category}`",
            f"   - Layer: `{finding.layer}`",
            f"   - Evidence: `{_redact_for_display(finding.evidence)}`",
            f"   - Location: `{location}`",
            f"   - Impact: {finding.impact}",
            f"   - Recommendation: {finding.recommendation}",
            f"   - Confidence: `{finding.confidence}`",
            "",
        ])

    lines.extend(["## Skills", ""])
    for skill in result.skills:
        lines.extend([
            f"### {skill.display_name}",
            "",
            f"- Path: `{skill.path}`",
            f"- Agent hints: `{', '.join(skill.agent_hints) or 'unknown'}`",
            f"- Words: `{skill.words}`",
            f"- Estimated index/load/runtime tokens: `{skill.estimated_index_tokens}` / `{skill.estimated_load_tokens}` / `{skill.estimated_runtime_tokens}`",
            f"- Highest priority: `{skill.highest_priority}`",
            "",
        ])

    return "\n".join(lines)


def render_html(result: ScanResult) -> str:
    findings_by_priority = {
        "P1": [finding for finding in result.findings if finding.priority == "P1"],
        "P2": [finding for finding in result.findings if finding.priority == "P2"],
        "P3": [finding for finding in result.findings if finding.priority == "P3"],
    }
    findings_by_layer = {
        "index": [finding for finding in result.findings if finding.layer == "index"],
        "load": [finding for finding in result.findings if finding.layer == "load"],
        "runtime": [finding for finding in result.findings if finding.layer == "runtime"],
    }
    max_count = max([1, *(len(items) for items in findings_by_priority.values())])

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Skills Doctor Report</title>
  <style>
    :root {{
      --bg: #f7f8fa;
      --panel: #ffffff;
      --ink: #1f2937;
      --muted: #64748b;
      --line: #d8dee8;
      --p1: #b42318;
      --p2: #b54708;
      --p3: #475467;
      --ok: #027a48;
      --accent: #175cd3;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font: 14px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    header {{
      background: #ffffff;
      border-bottom: 1px solid var(--line);
      padding: 28px 32px 22px;
    }}
    h1, h2, h3 {{ margin: 0; letter-spacing: 0; }}
    h1 {{ font-size: 28px; }}
    h2 {{ font-size: 18px; margin-bottom: 14px; }}
    h3 {{ font-size: 15px; }}
    .subhead {{ color: var(--muted); margin-top: 8px; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 24px; }}
    .grid {{ display: grid; gap: 16px; }}
    .metrics {{ grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); margin-bottom: 20px; }}
    .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
    }}
    .metric-value {{ font-size: 26px; font-weight: 700; }}
    .metric-label {{ color: var(--muted); margin-top: 4px; }}
    .section {{ margin-top: 22px; }}
    .split {{ grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }}
    .layer-card h3 {{ margin-bottom: 8px; }}
    .layer-card .metric-value {{ font-size: 22px; }}
    .bars {{ display: grid; gap: 10px; }}
    .bar-row {{ display: grid; grid-template-columns: 42px 1fr 36px; gap: 10px; align-items: center; }}
    .bar-track {{ height: 12px; background: #edf0f5; border-radius: 999px; overflow: hidden; }}
    .bar-fill {{ height: 100%; }}
    .fill-p1 {{ background: var(--p1); }}
    .fill-p2 {{ background: var(--p2); }}
    .fill-p3 {{ background: var(--p3); }}
    details {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      margin-bottom: 10px;
      overflow: hidden;
    }}
    summary {{
      cursor: pointer;
      list-style: none;
      padding: 14px 16px;
      display: grid;
      grid-template-columns: auto 1fr auto;
      gap: 12px;
      align-items: center;
    }}
    summary::-webkit-details-marker {{ display: none; }}
    .detail-body {{ border-top: 1px solid var(--line); padding: 14px 16px; }}
    .badge {{
      display: inline-flex;
      min-width: 34px;
      justify-content: center;
      border-radius: 999px;
      padding: 2px 8px;
      font-weight: 700;
      font-size: 12px;
      color: #fff;
    }}
    .p1 {{ background: var(--p1); }}
    .p2 {{ background: var(--p2); }}
    .p3 {{ background: var(--p3); }}
    .ok {{ background: var(--ok); }}
    .muted {{ color: var(--muted); }}
    code {{
      background: #f1f4f8;
      border: 1px solid #e3e8ef;
      border-radius: 5px;
      padding: 1px 5px;
      word-break: break-word;
    }}
    .kv {{ display: grid; grid-template-columns: 140px 1fr; gap: 8px 12px; }}
    .table {{ width: 100%; border-collapse: collapse; }}
    .table th, .table td {{ border-bottom: 1px solid var(--line); padding: 10px; text-align: left; vertical-align: top; }}
    .table th {{ color: var(--muted); font-weight: 600; }}
    .priority {{ font-weight: 700; }}
    .priority.P1 {{ color: var(--p1); }}
    .priority.P2 {{ color: var(--p2); }}
    .priority.P3 {{ color: var(--p3); }}
    footer {{ color: var(--muted); padding: 28px 32px; text-align: center; }}
    @media (max-width: 760px) {{
      header {{ padding: 22px 18px; }}
      main {{ padding: 16px; }}
      summary {{ grid-template-columns: 1fr; }}
      .kv {{ grid-template-columns: 1fr; }}
      .table {{ font-size: 13px; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Skills Doctor Report</h1>
    <div class="subhead">Generated {escape(result.generated_at)}. Local-only static inspection. Suggested actions are not applied automatically.</div>
  </header>
  <main>
    <section class="grid metrics">
      {_metric("Roots", result.summary.get("roots", 0))}
      {_metric("Skills", result.summary.get("skills", 0))}
      {_metric("Findings", result.summary.get("findings", 0))}
      {_metric("P1", result.summary.get("p1", 0))}
      {_metric("P2", result.summary.get("p2", 0))}
      {_metric("Estimated Total Tokens", result.summary.get("estimated_total_tokens", 0))}
    </section>

    <section class="section">
      <h2>Token Estimate by Loading Layer</h2>
      <p class="muted">Estimates use a rough chars / 4 heuristic for relative risk ranking, not billing.</p>
      <div class="grid split">
        {_layer_summary_card("Index Layer", "Always-visible name and description trigger surface.", result.summary.get("estimated_index_tokens", 0), len(findings_by_layer["index"]))}
        {_layer_summary_card("Load Layer", "SKILL.md body loaded after a skill is selected.", result.summary.get("estimated_load_tokens", 0), len(findings_by_layer["load"]))}
        {_layer_summary_card("Runtime Layer", "Potential references, scripts, assets, and command output loaded on demand.", result.summary.get("estimated_runtime_tokens", 0), len(findings_by_layer["runtime"]))}
      </div>
    </section>

    <section class="card section">
      <h2>Risk Distribution</h2>
      <div class="bars">
        {_bar("P1", len(findings_by_priority["P1"]), max_count, "fill-p1")}
        {_bar("P2", len(findings_by_priority["P2"]), max_count, "fill-p2")}
        {_bar("P3", len(findings_by_priority["P3"]), max_count, "fill-p3")}
      </div>
    </section>

    <section class="section">
      <h2>Findings by Loading Layer</h2>
      {_layer_findings_html("Index Layer", "Trigger metadata and skill selection risks.", findings_by_layer["index"])}
      {_layer_findings_html("Load Layer", "SKILL.md size, structure, and progressive disclosure risks.", findings_by_layer["load"])}
      {_layer_findings_html("Runtime Layer", "On-demand references, scripts, assets, secret, and command risks.", findings_by_layer["runtime"])}
    </section>

    <section class="section card">
      <h2>Skill Inventory</h2>
      {_skills_table(result.skills)}
    </section>

    <section class="section card">
      <h2>Scan Roots</h2>
      {_roots_table(result)}
    </section>
  </main>
  <footer>Generated by skills-doctor. Keep reports local if they contain private paths or project details.</footer>
</body>
</html>
"""


def write_output(content: str, output: str | None) -> None:
    if not output:
        print(content)
        return
    Path(output).write_text(content, encoding="utf-8")


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def _metric(label: str, value: object) -> str:
    return f"""<div class="card"><div class="metric-value">{escape(value)}</div><div class="metric-label">{escape(label)}</div></div>"""


def _layer_summary_card(title: str, description: str, tokens: object, findings_count: int) -> str:
    return f"""
<div class="card layer-card">
  <h3>{escape(title)}</h3>
  <div class="metric-value">{escape(tokens)}</div>
  <div class="metric-label">estimated tokens</div>
  <p class="muted">{escape(description)}</p>
  <div>{escape(findings_count)} findings</div>
</div>
"""


def _bar(label: str, value: int, max_count: int, css_class: str) -> str:
    width = int((value / max_count) * 100) if max_count else 0
    return f"""<div class="bar-row"><div>{escape(label)}</div><div class="bar-track"><div class="bar-fill {css_class}" style="width:{width}%"></div></div><div>{value}</div></div>"""


def _layer_findings_html(title: str, description: str, findings: list[Finding]) -> str:
    return f"""
<section class="card section">
  <h3>{escape(title)}</h3>
  <p class="muted">{escape(description)}</p>
  {_findings_html(findings)}
</section>
"""


def _findings_html(findings: list[Finding]) -> str:
    if not findings:
        return '<div class="card"><span class="badge ok">OK</span> No findings detected.</div>'
    items = []
    for finding in findings:
        location = finding.path if finding.line is None else f"{finding.path}:{finding.line}"
        items.append(f"""
<details>
  <summary>
    <span class="badge {finding.priority.lower()}">{escape(finding.priority)}</span>
    <strong>{escape(finding.title)}</strong>
    <span class="muted">{escape(finding.category)} · {escape(finding.confidence)}</span>
  </summary>
  <div class="detail-body kv">
    <div class="muted">Location</div><div><code>{escape(location)}</code></div>
    <div class="muted">Evidence</div><div><code>{escape(_redact_for_display(finding.evidence))}</code></div>
    <div class="muted">Impact</div><div>{escape(finding.impact)}</div>
    <div class="muted">Suggestion</div><div>{escape(finding.recommendation)}</div>
  </div>
</details>
""")
    return "\n".join(items)


def _skills_table(skills: list[SkillRecord]) -> str:
    if not skills:
        return '<p class="muted">No skills found in the scanned roots.</p>'
    rows = []
    for skill in sorted(skills, key=lambda item: (item.highest_priority, item.display_name)):
        rows.append(f"""
<tr>
  <td><strong>{escape(skill.display_name)}</strong><br><span class="muted">{escape(skill.description[:180])}</span></td>
  <td><code>{escape(skill.path)}</code></td>
  <td>{escape(", ".join(skill.agent_hints) or "unknown")}</td>
  <td>{escape(skill.estimated_index_tokens)}</td>
  <td>{escape(skill.estimated_load_tokens)}</td>
  <td>{escape(skill.estimated_runtime_tokens)}</td>
  <td><span class="priority {escape(skill.highest_priority)}">{escape(skill.highest_priority)}</span></td>
</tr>
""")
    return f"""
<table class="table">
  <thead><tr><th>Skill</th><th>Path</th><th>Agent</th><th>Index Est.</th><th>Load Est.</th><th>Runtime Est.</th><th>Status</th></tr></thead>
  <tbody>{''.join(rows)}</tbody>
</table>
"""


def _roots_table(result: ScanResult) -> str:
    if not result.roots:
        return '<p class="muted">No roots were scanned.</p>'
    rows = []
    for root in result.roots:
        rows.append(f"""
<tr>
  <td><code>{escape(root.path)}</code></td>
  <td>{escape(root.exists)}</td>
  <td>{escape(root.agent_hint)}</td>
  <td>{escape(root.scanned_skills)}</td>
  <td>{escape(", ".join(root.notes))}</td>
</tr>
""")
    return f"""
<table class="table">
  <thead><tr><th>Root</th><th>Exists</th><th>Agent</th><th>Skills</th><th>Notes</th></tr></thead>
  <tbody>{''.join(rows)}</tbody>
</table>
"""


def _redact_for_display(value: str) -> str:
    redacted = value
    if "[redacted-pattern]" in redacted:
        return "[redacted sensitive evidence]"
    secret_markers = ("sk-", "api_key", "apikey", "access_token", "secret", "password", "bearer")
    for marker in secret_markers:
        if marker.lower() in redacted.lower():
            return "[redacted sensitive evidence]"
    return redacted


def _review_pack_data(result: ScanResult) -> dict[str, object]:
    files: list[str] = []
    seen: set[str] = set()
    for finding in result.findings:
        if finding.priority not in {"P1", "P2"}:
            continue
        if finding.category not in {"safety", "trigger", "trigger-conflict", "structure", "token-cost"}:
            continue
        if finding.path in seen:
            continue
        seen.add(finding.path)
        files.append(finding.path)
    return {
        "mode": "read-only",
        "instructions": [
            "Do not edit, delete, move, install, uninstall, overwrite, or patch user skill files.",
            "Read only suspicious or representative files needed to confirm scanner findings.",
            "Return exact paths, evidence, impact, and suggested next edits for user approval.",
        ],
        "files_to_inspect": files[:20],
    }


def _review_files_html(files: list[str]) -> str:
    if not files:
        return '<p class="muted">No high-risk files detected.</p>'
    items = "".join(f"<li><code>{escape(path)}</code></li>" for path in files)
    return f"<ul>{items}</ul>"
