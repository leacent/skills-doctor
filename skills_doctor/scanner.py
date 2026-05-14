from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from pathlib import Path

from .analyzer import analyze_scan
from .defaults import DEFAULT_ROOTS, RESOURCE_DIRS
from .models import ResourceStats, RootRecord, ScanResult, SkillRecord


def scan_paths(paths: list[str] | None = None, max_depth: int = 4) -> ScanResult:
    roots = _resolve_roots(paths)
    root_records: list[RootRecord] = []
    skills: list[SkillRecord] = []

    for root in roots:
        root_record = RootRecord(
            path=str(root),
            exists=root.exists(),
            agent_hint=_infer_agent_hint(root),
        )
        root_records.append(root_record)

        if not root.exists():
            root_record.notes.append("path does not exist")
            continue
        if not root.is_dir():
            root_record.notes.append("path is not a directory")
            continue

        skill_dirs = _find_skill_dirs(root, max_depth=max_depth)
        root_record.scanned_skills = len(skill_dirs)
        for skill_dir in skill_dirs:
            skills.append(_read_skill(root, skill_dir))

    result = ScanResult(
        generated_at=datetime.now(timezone.utc).isoformat(),
        roots=root_records,
        skills=skills,
        findings=[],
        summary={},
    )
    return analyze_scan(result)


def _resolve_roots(paths: list[str] | None) -> list[Path]:
    raw_paths = paths if paths else [str(path) for path in DEFAULT_ROOTS if path.exists()]
    resolved: list[Path] = []
    seen: set[str] = set()
    for raw_path in raw_paths:
        path = Path(raw_path).expanduser()
        key = str(path.resolve()) if path.exists() else str(path)
        if key in seen:
            continue
        seen.add(key)
        resolved.append(path)
    return resolved


def _find_skill_dirs(root: Path, max_depth: int) -> list[Path]:
    if (root / "SKILL.md").is_file():
        return [root]

    found: list[Path] = []
    root_depth = len(root.parts)
    for current, dirnames, filenames in os.walk(root):
        current_path = Path(current)
        depth = len(current_path.parts) - root_depth
        if depth > max_depth:
            dirnames[:] = []
            continue
        if "SKILL.md" in filenames:
            found.append(current_path)
            dirnames[:] = []
            continue
        dirnames[:] = [name for name in dirnames if name not in {"node_modules", ".git", "__pycache__"}]
    return sorted(found)


def _read_skill(root: Path, skill_dir: Path) -> SkillRecord:
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    frontmatter, frontmatter_valid = _parse_frontmatter(text)
    body = _strip_frontmatter(text)
    encoded = text.encode("utf-8", errors="replace")
    words = len(re.findall(r"\b[\w-]+\b", body))
    resources = {name: _resource_stats(skill_dir / name) for name in RESOURCE_DIRS}
    estimated_index_tokens = _estimate_tokens(f"{frontmatter.get('name', '')}\n{frontmatter.get('description', '')}")
    estimated_load_tokens = _estimate_tokens(text)
    estimated_runtime_tokens = sum(_estimate_tokens_from_bytes(stats.total_bytes) for stats in resources.values())

    return SkillRecord(
        root=str(root),
        path=str(skill_dir),
        skill_md_path=str(skill_md),
        name=frontmatter.get("name", ""),
        description=frontmatter.get("description", ""),
        frontmatter=frontmatter,
        frontmatter_valid=frontmatter_valid,
        agent_hints=sorted(set([_infer_agent_hint(root), _infer_agent_hint(skill_dir)]) - {"unknown"}),
        chars=len(text),
        bytes=len(encoded),
        words=words,
        estimated_tokens=estimated_load_tokens,
        estimated_index_tokens=estimated_index_tokens,
        estimated_load_tokens=estimated_load_tokens,
        estimated_runtime_tokens=estimated_runtime_tokens,
        estimated_total_tokens=estimated_index_tokens + estimated_load_tokens + estimated_runtime_tokens,
        line_count=text.count("\n") + 1,
        resources=resources,
    )


def _parse_frontmatter(text: str) -> tuple[dict[str, str], bool]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, False

    end = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = index
            break
    if end is None:
        return {}, False

    data: dict[str, str] = {}
    frontmatter_lines = lines[1:end]
    index = 0
    while index < len(frontmatter_lines):
        line = frontmatter_lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        if ":" not in line:
            index += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key:
            if value in {"|", ">"}:
                block_lines: list[str] = []
                index += 1
                while index < len(frontmatter_lines):
                    next_line = frontmatter_lines[index]
                    if next_line and not next_line[0].isspace() and ":" in next_line:
                        index -= 1
                        break
                    block_lines.append(next_line.strip())
                    index += 1
                data[key] = "\n".join(block_lines).strip() if value == "|" else " ".join(block_lines).strip()
            else:
                data[key] = value
        index += 1
    return data, True


def _strip_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "\n".join(lines[index + 1 :])
    return text


def _resource_stats(path: Path) -> ResourceStats:
    stats = ResourceStats()
    if not path.exists() or not path.is_dir():
        return stats

    for file_path in sorted(path.rglob("*")):
        if not file_path.is_file():
            continue
        try:
            size = file_path.stat().st_size
        except OSError:
            size = 0
        stats.count += 1
        stats.total_bytes += size
        if size > stats.largest_file_bytes:
            stats.largest_file = str(file_path)
            stats.largest_file_bytes = size
        stats.files.append(str(file_path))
    return stats


def _estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4) if text else 0


def _estimate_tokens_from_bytes(size: int) -> int:
    return max(0, size // 4)


def _infer_agent_hint(path: Path) -> str:
    normalized = str(path).lower()
    if ".codex" in normalized:
        return "codex"
    if ".claude" in normalized:
        return "claude-code"
    if ".cursor" in normalized:
        return "cursor"
    if "windsurf" in normalized:
        return "windsurf"
    return "unknown"
