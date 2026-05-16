from __future__ import annotations

from pathlib import Path


DEFAULT_ROOTS = (
    Path(".codex/skills"),
    Path(".claude/skills"),
    Path(".cursor/skills"),
    Path.home() / ".codex" / "skills",
    Path.home() / ".claude" / "skills",
    Path.home() / ".cursor" / "skills",
)


RESOURCE_DIRS = ("references", "scripts", "assets")


DANGEROUS_PATTERNS = (
    "rm -rf",
    "sudo rm",
    "chmod 777",
    "curl | sh",
    "curl -fsSL",
    "wget | sh",
    "dd if=",
    "mkfs",
    "git reset --hard",
)


SECRET_PATTERNS = (
    "api_key",
    "apikey",
    "access_token",
    "secret_key",
    "private_key",
    "password=",
    "bearer ",
    "sk-",
)
