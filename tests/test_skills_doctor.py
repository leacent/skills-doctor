from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from skills_doctor.cli import main
from skills_doctor.report import render_html, render_json
from skills_doctor.scanner import scan_paths


class SkillsDoctorTests(unittest.TestCase):
    def test_scans_skill_and_reports_trigger_issue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".codex" / "skills"
            skill = root / "weak-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                """---
name: Weak Skill
description: helps with tasks
---

# Weak Skill

TODO: explain this skill.
""",
                encoding="utf-8",
            )

            result = scan_paths([str(root)])

            self.assertEqual(result.summary["skills"], 1)
            titles = {finding.title for finding in result.findings}
            self.assertIn("Skill name is not portable", titles)
            self.assertIn("Description is too short", titles)
            self.assertIn("Description uses weak trigger language", titles)

    def test_html_report_redacts_sensitive_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            skill = root / "secret-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                """---
name: secret-skill
description: Use when checking whether local AI agent skills contain sensitive examples or unsafe commands.
---

# Secret Skill

Example: api_key=sk-test-123456
""",
                encoding="utf-8",
            )

            result = scan_paths([str(root)])
            html = render_html(result)

            self.assertIn("Skills Doctor Report", html)
            self.assertIn("[redacted sensitive evidence]", html)
            self.assertNotIn("sk-test-123456", html)

    def test_json_output_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            skill = root / "good-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                """---
name: good-skill
description: Use when the user asks to inspect a narrow example skill for test coverage in skills-doctor.
---

# Good Skill

Do one thing.
""",
                encoding="utf-8",
            )

            result = scan_paths([str(root)])
            payload = json.loads(render_json(result))

            self.assertEqual(payload["summary"]["skills"], 1)
            self.assertEqual(payload["skills"][0]["name"], "good-skill")
            self.assertIn("estimated_index_tokens", payload["skills"][0])
            self.assertIn("estimated_load_tokens", payload["skills"][0])
            self.assertIn("estimated_runtime_tokens", payload["skills"][0])
            self.assertIn("estimated_total_tokens", payload["summary"])

    def test_layered_token_findings_and_html_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            skill = root / "heavy-skill"
            references = skill / "references"
            references.mkdir(parents=True)
            long_description = "Use when auditing local skills. " * 25
            (skill / "SKILL.md").write_text(
                f"""---
name: heavy-skill
description: {long_description}
---

# Heavy Skill

Read all references before answering.
""",
                encoding="utf-8",
            )
            (references / "large-reference.md").write_text("x" * 120_001, encoding="utf-8")

            result = scan_paths([str(root)])
            titles = {finding.title for finding in result.findings}
            layers = {finding.layer for finding in result.findings}
            html = render_html(result)

            self.assertIn("Description is too long", titles)
            self.assertIn("Single resource file is large", titles)
            self.assertIn("References are loaded too eagerly", titles)
            self.assertIn("index", layers)
            self.assertIn("runtime", layers)
            self.assertGreater(result.summary["estimated_index_tokens"], 0)
            self.assertGreater(result.summary["estimated_runtime_tokens"], 0)
            self.assertIn("Index Layer", html)
            self.assertIn("Load Layer", html)
            self.assertIn("Runtime Layer", html)

    def test_frontmatter_block_scalar_description(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            skill = root / "block-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                """---
name: block-skill
description: |
  Use when the user asks to inspect a skill whose description uses
  YAML block scalar syntax in frontmatter.
---

# Block Skill
""",
                encoding="utf-8",
            )

            result = scan_paths([str(root)])

            self.assertEqual(result.summary["skills"], 1)
            self.assertIn("YAML block scalar syntax", result.skills[0].description)
            titles = {finding.title for finding in result.findings}
            self.assertNotIn("Missing trigger description", titles)

    def test_cli_writes_html_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            skill = root / "sample-skill"
            output = Path(tmp) / "report.html"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                """---
name: sample-skill
description: Use when generating a sample local skills inspection report for CLI integration tests.
---

# Sample Skill
""",
                encoding="utf-8",
            )

            code = main(["report", str(root), "--output", str(output)])

            self.assertEqual(code, 0)
            self.assertTrue(output.exists())
            self.assertIn("Skills Doctor Report", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
