from __future__ import annotations

import re
from pathlib import Path

from .defaults import (
    DANGEROUS_PATTERNS,
    OVERBROAD_PHRASES,
    SECRET_PATTERNS,
    STOPWORDS,
    WEAK_DESCRIPTION_PHRASES,
)
from .models import Finding, ScanResult, SkillRecord


def analyze_scan(result: ScanResult) -> ScanResult:
    all_findings: list[Finding] = []
    for skill in result.skills:
        skill.findings.extend(_analyze_skill(skill))
        all_findings.extend(skill.findings)

    conflict_findings = _analyze_conflicts(result.skills)
    all_findings.extend(conflict_findings)
    result.findings = sorted(all_findings, key=lambda finding: finding.sort_key())
    result.summary = _build_summary(result)
    return result


def _analyze_skill(skill: SkillRecord) -> list[Finding]:
    findings: list[Finding] = []
    text = Path(skill.skill_md_path).read_text(encoding="utf-8", errors="replace")
    lower = text.lower()

    if not skill.frontmatter_valid:
        findings.append(_finding(
            "P1",
            "structure",
            "load",
            "Missing or invalid frontmatter",
            skill.skill_md_path,
            "SKILL.md should start with YAML frontmatter delimited by ---.",
            "Agents may not discover or trigger this skill reliably.",
            "Add frontmatter with at least name and description.",
            "high",
        ))

    if not skill.name:
        findings.append(_finding(
            "P1",
            "structure",
            "index",
            "Missing skill name",
            skill.skill_md_path,
            "frontmatter.name is missing.",
            "Agents and registries need a stable skill identity.",
            "Add a lowercase, hyphenated, domain-specific name.",
            "high",
        ))
    elif not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,62}[a-z0-9]", skill.name):
        findings.append(_finding(
            "P2",
            "structure",
            "index",
            "Skill name is not portable",
            skill.skill_md_path,
            f"name={skill.name!r}",
            "Names with spaces, uppercase letters, or long identifiers are harder to install across agents.",
            "Use a lowercase hyphenated name under 64 characters.",
        ))

    if not skill.description:
        findings.append(_finding(
            "P1",
            "trigger",
            "index",
            "Missing trigger description",
            skill.skill_md_path,
            "frontmatter.description is missing.",
            "The description is the primary trigger surface for most skill systems.",
            "Write a concise description that says what the skill does and when to use it.",
            "high",
        ))
    else:
        desc_lower = skill.description.lower()
        if len(skill.description) > 500:
            findings.append(_finding(
                "P2",
                "trigger",
                "index",
                "Description is too long",
                skill.skill_md_path,
                f"description has {len(skill.description)} characters, estimated {skill.estimated_index_tokens} index tokens.",
                "Long descriptions increase the always-visible index surface and can distract trigger selection.",
                "Compress the description into concrete positive triggers plus a short non-use boundary.",
            ))
        if len(skill.description) < 80:
            findings.append(_finding(
                "P2",
                "trigger",
                "index",
                "Description is too short",
                skill.skill_md_path,
                f"description has {len(skill.description)} characters.",
                "Short descriptions usually lack enough trigger boundaries.",
                "Include the task, trigger intent, artifact type, and non-use boundary.",
            ))
        if any(phrase in desc_lower for phrase in WEAK_DESCRIPTION_PHRASES):
            findings.append(_finding(
                "P2",
                "trigger",
                "index",
                "Description uses weak trigger language",
                skill.skill_md_path,
                _matched_phrase(desc_lower, WEAK_DESCRIPTION_PHRASES),
                "Weak language can cause over-triggering or under-triggering.",
                "Replace generic phrasing with concrete user intents and artifacts.",
            ))
        if any(phrase in desc_lower for phrase in OVERBROAD_PHRASES):
            findings.append(_finding(
                "P2",
                "trigger",
                "index",
                "Description appears over-broad",
                skill.skill_md_path,
                _matched_phrase(desc_lower, OVERBROAD_PHRASES),
                "Over-broad skills distract the agent and can conflict with specialized skills.",
                "Add clear positive and negative trigger boundaries.",
            ))

    if skill.words > 5000:
        findings.append(_finding(
            "P1",
            "token-cost",
            "load",
            "SKILL.md is extremely large",
            skill.skill_md_path,
            f"{skill.words} words, estimated {skill.estimated_tokens} tokens.",
            "Large skill bodies consume context and make triggering expensive.",
            "Move examples, schemas, and variants into references loaded only when needed.",
            "high",
        ))
    elif skill.words > 3000:
        findings.append(_finding(
            "P2",
            "token-cost",
            "load",
            "SKILL.md is large",
            skill.skill_md_path,
            f"{skill.words} words, estimated {skill.estimated_tokens} tokens.",
            "Large skill bodies can increase token cost and reduce attention on the current task.",
            "Keep SKILL.md procedural and move long detail into references.",
        ))

    references = skill.resources.get("references")
    if skill.words > 1800 and references and references.count == 0:
        findings.append(_finding(
            "P2",
            "progressive-disclosure",
            "load",
            "Long skill lacks reference split",
            skill.skill_md_path,
            f"{skill.words} words with no reference files detected.",
            "Agents may need to load too much content up front.",
            "Move deep examples, policies, and variant-specific material into references/.",
        ))

    if "read all references" in lower or "load all references" in lower:
        findings.append(_finding(
            "P2",
            "progressive-disclosure",
            "runtime",
            "References are loaded too eagerly",
            skill.skill_md_path,
            "Instruction asks the agent to read/load all references.",
            "Eager loading increases token cost even when most references are irrelevant.",
            "Tell the agent when each reference should be read.",
        ))

    for dirname, stats in skill.resources.items():
        dir_path = Path(skill.path) / dirname
        if dir_path.exists() and dir_path.is_dir() and stats.count == 0:
            findings.append(_finding(
                "P3",
                "structure",
                "runtime",
                f"Empty {dirname}/ directory",
                str(dir_path),
                f"{dirname}/ exists but contains no files.",
                "Empty resource directories look unfinished and add maintenance noise.",
                "Remove the directory or add purposeful resources.",
                "high",
            ))
        if stats.total_bytes > 200_000:
            findings.append(_finding(
                "P2",
                "runtime-cost",
                "runtime",
                f"{dirname}/ resources are large",
                str(dir_path),
                f"{stats.count} files, {stats.total_bytes} bytes, estimated {stats.total_bytes // 4} runtime tokens if loaded.",
                "Large resource directories can create expensive runtime context when read into the conversation.",
                "Keep large examples or reference packs behind explicit, narrow load conditions.",
            ))
        if stats.largest_file_bytes > 100_000:
            findings.append(_finding(
                "P2",
                "runtime-cost",
                "runtime",
                "Single resource file is large",
                stats.largest_file,
                f"{stats.largest_file_bytes} bytes, estimated {stats.largest_file_bytes // 4} runtime tokens if loaded.",
                "A single large runtime file can dominate context once referenced.",
                "Split the file by task or replace it with a deterministic script that returns summaries.",
            ))

    if skill.estimated_runtime_tokens > 50_000:
        findings.append(_finding(
            "P2",
            "runtime-cost",
            "runtime",
            "Runtime context estimate is high",
            skill.path,
            f"estimated_runtime_tokens={skill.estimated_runtime_tokens}",
            "The skill has a large potential runtime context footprint across references, scripts, or assets.",
            "Add progressive disclosure rules and keep script outputs summarized.",
        ))

    for pattern in DANGEROUS_PATTERNS:
        if pattern in lower:
            findings.append(_finding(
                "P1",
                "safety",
                "runtime",
                "Dangerous command pattern",
                skill.skill_md_path,
                _redact(pattern),
                "Skills should not normalize destructive or privilege-escalating commands.",
                "Gate destructive operations behind explicit user confirmation and document safer alternatives.",
                "high",
                _line_for(text, pattern),
            ))

    secret_reported = False
    for pattern in SECRET_PATTERNS:
        if secret_reported:
            break
        if pattern in lower:
            findings.append(_finding(
                "P1",
                "safety",
                "runtime",
                "Potential sensitive value or secret pattern",
                skill.skill_md_path,
                _redact(pattern),
                "Skills and examples must not expose credentials or train agents to log secrets.",
                "Replace real values with placeholders and document environment-variable usage.",
                "medium",
                _line_for(lower, pattern),
            ))
            secret_reported = True

    absolute_path_match = re.search(r"(/Users/[^\s)`'\"]+|/home/[^\s)`'\"]+|[A-Za-z]:\\[^\s)`'\"]+)", text)
    if absolute_path_match:
        findings.append(_finding(
            "P2",
            "portability",
            "runtime",
            "Hardcoded absolute path",
            skill.skill_md_path,
            _redact(absolute_path_match.group(0)),
            "Hardcoded local paths reduce portability across machines and agents.",
            "Use relative paths, environment variables, or clearly mark local examples as examples.",
            "medium",
            _line_for(text, absolute_path_match.group(0)),
        ))

    if "todo" in lower or "fixme" in lower or "your skill" in lower:
        findings.append(_finding(
            "P3",
            "maintenance",
            "load",
            "Unfinished scaffold marker",
            skill.skill_md_path,
            "Detected TODO/FIXME/template wording.",
            "Unfinished markers reduce trust in the skill.",
            "Finish the section or remove the placeholder.",
        ))

    return findings


def _analyze_conflicts(skills: list[SkillRecord]) -> list[Finding]:
    findings: list[Finding] = []
    token_sets = {skill.path: _trigger_tokens(skill.description) for skill in skills if skill.description}
    pairs_checked = 0

    for index, left in enumerate(skills):
        for right in skills[index + 1 :]:
            if not left.description or not right.description:
                continue
            left_tokens = token_sets.get(left.path, set())
            right_tokens = token_sets.get(right.path, set())
            if not left_tokens or not right_tokens:
                continue
            score = len(left_tokens & right_tokens) / len(left_tokens | right_tokens)
            if score < 0.55:
                continue
            pairs_checked += 1
            if pairs_checked > 25:
                return findings
            evidence = f"{left.display_name} and {right.display_name} share trigger tokens: {', '.join(sorted(left_tokens & right_tokens)[:8])}"
            finding = Finding(
                priority="P2",
                category="conflict",
                layer="index",
                title="Potential trigger overlap",
                path=f"{left.skill_md_path} <> {right.skill_md_path}",
                evidence=evidence,
                impact="Overlapping trigger descriptions can cause multiple skills to activate or distract the agent.",
                recommendation="Narrow one or both descriptions with explicit positive and negative trigger boundaries.",
                confidence="medium",
            )
            left.findings.append(finding)
            right.findings.append(finding)
            findings.append(finding)
    return findings


def _build_summary(result: ScanResult) -> dict[str, int]:
    priorities = {"P1": 0, "P2": 0, "P3": 0}
    for finding in result.findings:
        if finding.priority in priorities:
            priorities[finding.priority] += 1
    return {
        "roots": len(result.roots),
        "skills": len(result.skills),
        "findings": len(result.findings),
        "p1": priorities["P1"],
        "p2": priorities["P2"],
        "p3": priorities["P3"],
        "estimated_tokens": sum(skill.estimated_tokens for skill in result.skills),
        "estimated_index_tokens": sum(skill.estimated_index_tokens for skill in result.skills),
        "estimated_load_tokens": sum(skill.estimated_load_tokens for skill in result.skills),
        "estimated_runtime_tokens": sum(skill.estimated_runtime_tokens for skill in result.skills),
        "estimated_total_tokens": sum(skill.estimated_total_tokens for skill in result.skills),
    }


def _finding(
    priority: str,
    category: str,
    layer: str,
    title: str,
    path: str,
    evidence: str,
    impact: str,
    recommendation: str,
    confidence: str = "medium",
    line: int | None = None,
) -> Finding:
    return Finding(
        priority=priority,
        category=category,
        layer=layer,
        title=title,
        path=path,
        evidence=evidence,
        impact=impact,
        recommendation=recommendation,
        confidence=confidence,
        line=line,
    )


def _matched_phrase(value: str, phrases: tuple[str, ...]) -> str:
    for phrase in phrases:
        if phrase in value:
            return f"matched phrase: {phrase}"
    return "matched weak phrase"


def _trigger_tokens(description: str) -> set[str]:
    words = re.findall(r"[a-z0-9][a-z0-9-]{2,}", description.lower())
    return {word for word in words if word not in STOPWORDS}


def _line_for(text: str, needle: str) -> int | None:
    lower_text = text.lower()
    lower_needle = needle.lower()
    offset = lower_text.find(lower_needle)
    if offset < 0:
        return None
    return text[:offset].count("\n") + 1


def _redact(value: str) -> str:
    if len(value) <= 8:
        return "[redacted-pattern]"
    return value[:4] + "[redacted]" + value[-2:]
