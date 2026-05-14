from __future__ import annotations

import argparse
import sys

from .report import render_result, write_output
from .scanner import scan_paths


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "command"):
        parser.print_help()
        return 2

    result = scan_paths(args.paths, max_depth=args.max_depth)
    output_format = args.format
    content = render_result(result, output_format)
    write_output(content, args.output)

    if args.output:
        print(f"skills-doctor wrote {output_format} report to {args.output}")

    if args.fail_on:
        rank = {"P1": 1, "P2": 2, "P3": 3}
        threshold = rank[args.fail_on]
        for finding in result.findings:
            if rank.get(finding.priority, 99) <= threshold:
                return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skills-doctor",
        description="Check local AI agent skills and generate best-practice reports.",
    )
    subparsers = parser.add_subparsers(dest="command")

    _add_scan_command(subparsers, "scan", default_format="markdown")
    _add_scan_command(subparsers, "review", default_format="markdown")
    _add_scan_command(subparsers, "check", default_format="html", default_output="skills-doctor-report.html")
    _add_scan_command(subparsers, "report", default_format="html", default_output="skills-doctor-report.html")

    return parser


def _add_scan_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    default_format: str,
    default_output: str | None = None,
) -> None:
    command = subparsers.add_parser(name)
    command.add_argument("paths", nargs="*", help="Skill roots or skill directories to scan.")
    command.add_argument(
        "--format",
        choices=("json", "markdown", "html"),
        default=default_format,
        help="Output format.",
    )
    command.add_argument(
        "--output",
        default=default_output,
        help="Output file. Omit to print to stdout.",
    )
    command.add_argument(
        "--max-depth",
        type=int,
        default=4,
        help="Maximum nested directory depth for discovering SKILL.md files.",
    )
    command.add_argument(
        "--fail-on",
        choices=("P1", "P2", "P3"),
        help="Exit with code 1 when findings at or above the priority are present.",
    )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

