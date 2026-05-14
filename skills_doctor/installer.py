from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from shutil import copytree
from typing import Any


SKILL_NAME = "skills-doctor"
TARGET_DIRS = {
    "claude": Path(".claude") / "skills" / SKILL_NAME,
    "codex": Path(".codex") / "skills" / SKILL_NAME,
    "cursor": Path(".cursor") / "skills" / SKILL_NAME,
}


@dataclass(frozen=True)
class InstallResult:
    target: str
    path: Path
    status: str


def expand_targets(target: str) -> list[str]:
    if target == "all":
        return list(TARGET_DIRS)
    if target not in TARGET_DIRS:
        raise ValueError(f"Unsupported target: {target}")
    return [target]


def install_skill(target: str, *, force: bool = False, dry_run: bool = False, home: Path | None = None) -> list[InstallResult]:
    home_dir = home or Path.home()
    results: list[InstallResult] = []

    for target_name in expand_targets(target):
        skill_dir = home_dir / TARGET_DIRS[target_name]
        skill_path = skill_dir / "SKILL.md"

        if dry_run:
            results.append(InstallResult(target_name, skill_path, "would-install"))
            continue

        if skill_path.exists() and not force:
            results.append(InstallResult(target_name, skill_path, "skipped"))
            continue

        skill_dir.parent.mkdir(parents=True, exist_ok=True)
        with resources.as_file(_packaged_skill_root()) as source_dir:
            copytree(source_dir, skill_dir, dirs_exist_ok=True)
        results.append(InstallResult(target_name, skill_path, "installed"))

    return results


def _read_packaged_skill() -> str:
    return _packaged_skill_root().joinpath("SKILL.md").read_text(encoding="utf-8")


def _packaged_skill_root() -> Any:
    return resources.files("skills_doctor").joinpath("resources", SKILL_NAME)
