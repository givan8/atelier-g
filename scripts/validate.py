#!/usr/bin/env python3
"""Structural validation for the atelier-g skill and role libraries.

Checks skills/<name>/SKILL.md and roles/<name>/ROLE.md for the properties we can
verify mechanically. Behaviour is checked separately by evals/run.py.

Standard library only, by design — see CLAUDE.md.

Usage:
    ./scripts/validate.py                  # everything
    ./scripts/validate.py review-code      # named skills or roles
    ./scripts/validate.py --skills-only
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
ROLES = ROOT / "roles"

MAX_LINES = 150
MAX_DESCRIPTION_WORDS = 60
ACCESS_VALUES = ("read-only", "read-write")

# Harness-specific markers. See docs/adr/0002-harness-neutral-skills.md.
# Crude by necessity: this is a tripwire, not a parser.
FORBIDDEN = {
    r"\bclaude code\b": "names a specific harness",
    r"\bcursor\b": "names a specific harness",
    r"\bcopilot\b": "names a specific harness",
    r"^\s*/[a-z][a-z-]{2,}\s*$": "looks like a slash command",
    r"</?(?:function_calls|invoke|parameter|antml|thinking|system-reminder|tool_use)\b":
        "harness-specific markup",
    r"\bthink step by step\b": "model-specific prompting",
    r"\byou are an? (?:expert|helpful|world-class)\b": "model-specific prompting",
    r"\b(?:gpt-[0-9]|claude-[0-9]|llama-[0-9]|gemini-[0-9])": "pins a model version",
}

RESERVED_PROSE = (
    "the agent should",
    "the assistant should",
    "the model should",
)


class Problem(Exception):
    pass


def parse_frontmatter(text: str) -> tuple[dict[str, str], int]:
    """Return (frontmatter, body_start_line). Minimal YAML: scalars and folded blocks."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise Problem("missing YAML frontmatter (file must start with '---')")

    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        raise Problem("frontmatter is not closed with '---'") from None

    data: dict[str, str] = {}
    key: str | None = None
    folded: list[str] = []

    for raw in lines[1:end]:
        if key and (raw.startswith((" ", "\t")) or not raw.strip()):
            folded.append(raw.strip())
            continue
        if key:
            data[key] = " ".join(p for p in folded if p).strip()
            key, folded = None, []
        if not raw.strip():
            continue
        if ":" not in raw:
            raise Problem(f"frontmatter line is not 'key: value': {raw!r}")
        k, _, v = raw.partition(":")
        k, v = k.strip(), v.strip()
        if v in (">", "|", ">-", "|-"):
            key, folded = k, []
        else:
            data[k] = v.strip("\"'")

    if key:
        data[key] = " ".join(p for p in folded if p).strip()

    return data, end + 1


def check(directory: Path, filename: str, required: tuple[str, ...],
          optional: tuple[str, ...], kind: str) -> list[str]:
    rel = f"{kind}/{directory.name}"
    problems: list[str] = []
    path = directory / filename

    if not path.exists():
        return [f"{rel}: no {filename}"]

    text = path.read_text(encoding="utf-8")

    try:
        fm, body_start = parse_frontmatter(text)
    except Problem as exc:
        return [f"{rel}: {exc}"]

    for field in required:
        if not fm.get(field):
            problems.append(f"{rel}: frontmatter is missing '{field}'")

    unknown = set(fm) - set(required) - set(optional)
    if unknown:
        problems.append(f"{rel}: unknown frontmatter keys: {', '.join(sorted(unknown))}")

    name = fm.get("name", "")
    if name and name != directory.name:
        problems.append(f"{rel}: frontmatter name is {name!r}, must match directory name")
    if name and not re.fullmatch(r"[a-z][a-z0-9]*(-[a-z0-9]+)*", name):
        problems.append(f"{rel}: name must be kebab-case")

    if "access" in required:
        access = fm.get("access", "")
        if access and access not in ACCESS_VALUES:
            problems.append(
                f"{rel}: access is {access!r}, must be one of {', '.join(ACCESS_VALUES)}"
            )

    description = fm.get("description", "")
    words = len(description.split())
    if description:
        if words > MAX_DESCRIPTION_WORDS:
            problems.append(
                f"{rel}: description is {words} words (max {MAX_DESCRIPTION_WORDS}) — "
                "it is a trigger, not a summary"
            )
        trigger = r"\buse\b|\bwhen\b" if kind == "skills" else r"\bdispatch\b|\bwhen\b"
        if not re.search(trigger, description, re.I):
            problems.append(
                f"{rel}: description should state when this applies so a harness "
                "can match on it"
            )

    body = "\n".join(text.split("\n")[body_start:])
    body_lines = body.strip().split("\n")

    if len(body_lines) > MAX_LINES:
        problems.append(
            f"{rel}: body is {len(body_lines)} lines (max {MAX_LINES}) — "
            "split it, or move detail into a linked reference file"
        )

    if not body.strip():
        problems.append(f"{rel}: body is empty")
    elif not body_lines[0].startswith("# "):
        problems.append(f"{rel}: body must open with a level-1 heading")

    if kind == "roles":
        for heading in ("You may not",):
            if heading.lower() not in body.lower():
                problems.append(
                    f"{rel}: charter has no '{heading}' section — a role without "
                    "boundaries collapses into doing the whole thing"
                )

    in_fence = False
    for i, line in enumerate(body_lines, start=body_start + 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for pattern, why in FORBIDDEN.items():
            if re.search(pattern, line, re.I | re.M):
                problems.append(f"{rel}:{i}: {why} — see ADR-0002 ({line.strip()[:60]!r})")
        for phrase in RESERVED_PROSE:
            if phrase in line.lower():
                problems.append(
                    f"{rel}:{i}: write in the second person ('you'), not {phrase!r}"
                )

    for target in re.findall(r"\]\((\.\.?/[^)#]+)", body):
        if not (directory / target).resolve().exists():
            problems.append(f"{rel}: broken relative link to {target}")

    return problems


def dirs_in(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted(d for d in root.iterdir() if d.is_dir() and not d.name.startswith("."))


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    flags = {a for a in argv[1:] if a.startswith("--")}

    targets: list[tuple[Path, str, tuple[str, ...], tuple[str, ...], str]] = []
    if "--roles-only" not in flags:
        for d in dirs_in(SKILLS):
            targets.append((d, "SKILL.md", ("name", "description"),
                            ("when_to_use", "version"), "skills"))
    if "--skills-only" not in flags:
        for d in dirs_in(ROLES):
            targets.append((d, "ROLE.md", ("name", "description", "access"),
                            ("model", "effort"), "roles"))

    if args:
        targets = [t for t in targets if t[0].name in args]
        missing = set(args) - {t[0].name for t in targets}
        if missing:
            print(f"no such skill or role: {', '.join(sorted(missing))}", file=sys.stderr)
            return 2

    if not targets:
        print("nothing to validate", file=sys.stderr)
        return 2

    problems: list[str] = []
    for directory, filename, required, optional, kind in targets:
        problems.extend(check(directory, filename, required, optional, kind))

    if problems:
        for p in problems:
            print(f"FAIL {p}")
        print(f"\n{len(problems)} problem(s) across {len(targets)} file(s)")
        return 1

    skills = sum(1 for t in targets if t[4] == "skills")
    roles = sum(1 for t in targets if t[4] == "roles")
    print(f"OK  {skills} skill(s) and {roles} role(s) validated")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
