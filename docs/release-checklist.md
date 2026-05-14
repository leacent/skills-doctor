# Release Checklist

Use this checklist before publishing a GitHub release.

- Run `python3 -m unittest`.
- Run `python3 -m skills_doctor report . --output /tmp/skills-doctor-report.html`.
- Open the generated HTML report locally and confirm it renders.
- Confirm no real secrets appear in examples, tests, docs, or reports.
- Confirm `skill/SKILL.md` trigger remains narrow.
- Tag the release.

