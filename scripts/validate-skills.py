#!/usr/bin/env python3
"""Structural validation for the atelier-g skill library.

Checks every skills/<name>/SKILL.md for the properties we can verify
mechanically. Behaviour is checked separately by evals/run.py.

Standard library only, by design — see CLAUDE.md.

Usage:
    ./scripts/validate-skills.py            # validate all skills
    ./scripts/validate-skills.py review-code
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

MAX_LINES = 150
MAX_DESCRIPTION_WORDS = 60
REQUIRED_KEYS = ("name", "description")
OPTIONAL_KEYS = ("when_to_use", "version")

# Harness-specific markers. See docs/adr/0002-harness-neutral-skills.md.
# Crude by necessity: this is a tripwire, not a parser.
FORBIDDEN = {
    r"\bclaude code\b": "names a specific harness",
    r"\bcursor\b": "names a specific harness",
    r"\bcopilot\b": "names a specific harness",
    r"^\s*/[a-z][a-z-]{2,}\s*$": "looks like a slash command",
    (
        r"</?(?:function_calls|invoke|parameter|antml|thinking|system-reminder|tool_use)\b"
    ): "harness-specific markup",
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


def parse_frontmatter(text: str, rel: str) -> tuple[dict[str, str], int]:
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


def check(skill_dir: Path) -> list[str]:
    rel = skill_dir.name
    problems: list[str] = []
    path = skill_dir / "SKILL.md"

    if not path.exists():
        return [f"{rel}: no SKILL.md"]

    text = path.read_text(encoding="utf-8")

    try:
        fm, body_start = parse_frontmatter(text, rel)
    except Problem as exc:
        return [f"{rel}: {exc}"]

    for required in REQUIRED_KEYS:
        if not fm.get(required):
            problems.append(f"{rel}: frontmatter is missing '{required}'")

    unknown = set(fm) - set(REQUIRED_KEYS) - set(OPTIONAL_KEYS)
    if unknown:
        problems.append(f"{rel}: unknown frontmatter keys: {', '.join(sorted(unknown))}")

    name = fm.get("name", "")
    if name and name != rel:
        problems.append(f"{rel}: frontmatter name is {name!r}, must match directory name")
    if name and not re.fullmatch(r"[a-z][a-z0-9]*(-[a-z0-9]+)*", name):
        problems.append(f"{rel}: name must be kebab-case")

    description = fm.get("description", "")
    words = len(description.split())
    if description:
        if words > MAX_DESCRIPTION_WORDS:
            problems.append(
                f"{rel}: description is {words} words (max {MAX_DESCRIPTION_WORDS}) — "
                "it is a trigger, not a summary"
            )
        if not re.search(r"\buse\b|\bwhen\b", description, re.I):
            problems.append(
                f"{rel}: description should state when to use the skill "
                "(e.g. 'Use when …') so a harness can match on it"
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
        if not (skill_dir / target).resolve().exists():
            problems.append(f"{rel}: broken relative link to {target}")

    return problems


def main(argv: list[str]) -> int:
    if not SKILLS.is_dir():
        print(f"no skills directory at {SKILLS}", file=sys.stderr)
        return 2

    wanted = set(argv[1:])
    dirs = sorted(d for d in SKILLS.iterdir() if d.is_dir() and not d.name.startswith("."))
    if wanted:
        dirs = [d for d in dirs if d.name in wanted]
        missing = wanted - {d.name for d in dirs}
        if missing:
            print(f"no such skill: {', '.join(sorted(missing))}", file=sys.stderr)
            return 2

    all_problems: list[str] = []
    for d in dirs:
        all_problems.extend(check(d))

    if all_problems:
        for p in all_problems:
            print(f"FAIL {p}")
        print(f"\n{len(all_problems)} problem(s) across {len(dirs)} skill(s)")
        return 1

    print(f"OK  {len(dirs)} skill(s) validated")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
