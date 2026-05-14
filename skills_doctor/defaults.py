from __future__ import annotations

from pathlib import Path


DEFAULT_ROOTS = (
    Path(".codex/skills"),
    Path(".claude/skills"),
    Path(".cursor/rules"),
    Path.home() / ".codex" / "skills",
    Path.home() / ".claude" / "skills",
    Path.home() / ".cursor" / "rules",
)


RESOURCE_DIRS = ("references", "scripts", "assets")


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "use",
    "when",
    "with",
    "you",
    "user",
    "users",
    "skill",
    "skills",
    "agent",
    "agents",
}


WEAK_DESCRIPTION_PHRASES = (
    "helps with",
    "best practices",
    "general guidance",
    "various tasks",
    "anything",
    "all tasks",
    "any task",
    "useful for",
    "common tasks",
)


OVERBROAD_PHRASES = (
    "always use",
    "use for any",
    "use for all",
    "every request",
    "all coding tasks",
    "all design tasks",
    "all tasks",
    "anything related",
)


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

