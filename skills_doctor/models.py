from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class Finding:
    priority: str
    category: str
    layer: str
    title: str
    path: str
    evidence: str
    impact: str
    recommendation: str
    confidence: str = "medium"
    line: int | None = None

    def sort_key(self) -> tuple[int, str, str]:
        rank = {"P1": 0, "P2": 1, "P3": 2}.get(self.priority, 9)
        return rank, self.category, self.title


@dataclass
class ResourceStats:
    count: int = 0
    total_bytes: int = 0
    largest_file: str = ""
    largest_file_bytes: int = 0
    files: list[str] = field(default_factory=list)


@dataclass
class SkillRecord:
    root: str
    path: str
    skill_md_path: str
    name: str
    description: str
    frontmatter: dict[str, str]
    frontmatter_valid: bool
    agent_hints: list[str]
    chars: int
    bytes: int
    words: int
    estimated_tokens: int
    estimated_index_tokens: int
    estimated_load_tokens: int
    estimated_runtime_tokens: int
    estimated_total_tokens: int
    line_count: int
    resources: dict[str, ResourceStats]
    findings: list[Finding] = field(default_factory=list)

    @property
    def display_name(self) -> str:
        return self.name or Path(self.path).name

    @property
    def highest_priority(self) -> str:
        if any(f.priority == "P1" for f in self.findings):
            return "P1"
        if any(f.priority == "P2" for f in self.findings):
            return "P2"
        if any(f.priority == "P3" for f in self.findings):
            return "P3"
        return "OK"


@dataclass
class RootRecord:
    path: str
    exists: bool
    agent_hint: str
    scanned_skills: int = 0
    notes: list[str] = field(default_factory=list)


@dataclass
class ScanResult:
    generated_at: str
    roots: list[RootRecord]
    skills: list[SkillRecord]
    findings: list[Finding]
    summary: dict[str, Any]

    @classmethod
    def empty(cls) -> "ScanResult":
        return cls(
            generated_at=datetime.now(timezone.utc).isoformat(),
            roots=[],
            skills=[],
            findings=[],
            summary={
                "roots": 0,
                "skills": 0,
                "findings": 0,
                "p1": 0,
                "p2": 0,
                "p3": 0,
                "estimated_tokens": 0,
                "estimated_index_tokens": 0,
                "estimated_load_tokens": 0,
                "estimated_runtime_tokens": 0,
                "estimated_total_tokens": 0,
            },
        )
