#!/usr/bin/env python3
"""Run skill eval cases.

A case is a task plus assertions about a correct response. This runner does not
call a model — deliberately. It has two jobs:

  1. emit    turn cases into prompt files a harness (or a person) can run
  2. check   score recorded outputs against the case's assertions

Keeping the model out of the runner means the same cases work with any harness,
in CI, or with a human writing the response by hand. See docs/architecture.md.

Cases are TOML (stdlib `tomllib`, Python 3.11+). Outputs are plain text in
evals/outputs/<case-id>.txt.

Usage:
    ./evals/run.py                        # score every case with a recording
    ./evals/run.py --skill review-code    # only that skill's cases
    ./evals/run.py --emit ./prompts       # write prompt files to run
    ./evals/run.py --strict               # missing recordings fail (CI)
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "evals" / "cases"
OUTPUTS = ROOT / "evals" / "outputs"
SKILLS = ROOT / "skills"


@dataclass
class Case:
    id: str
    skill: str
    prompt: str
    rationale: str = ""
    expect_contains: list[str] = field(default_factory=list)
    expect_absent: list[str] = field(default_factory=list)
    expect_matches: list[str] = field(default_factory=list)

    @classmethod
    def load(cls, path: Path) -> "Case":
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        missing = {"skill", "prompt"} - set(data)
        if missing:
            raise ValueError(f"{path.name}: missing key(s): {', '.join(sorted(missing))}")
        if not (SKILLS / data["skill"] / "SKILL.md").exists():
            raise ValueError(f"{path.name}: references unknown skill {data['skill']!r}")
        if not any(k in data for k in ("expect_contains", "expect_absent", "expect_matches")):
            raise ValueError(f"{path.name}: has no assertions — it cannot fail, so it is not a test")
        return cls(
            id=path.stem,
            skill=data["skill"],
            prompt=data["prompt"].strip(),
            rationale=data.get("rationale", "").strip(),
            expect_contains=data.get("expect_contains", []),
            expect_absent=data.get("expect_absent", []),
            expect_matches=data.get("expect_matches", []),
        )

    def score(self, output: str) -> list[str]:
        """Return a list of failures. Empty means pass."""
        low = output.lower()
        failures = []
        for needle in self.expect_contains:
            if needle.lower() not in low:
                failures.append(f"missing expected text: {needle!r}")
        for needle in self.expect_absent:
            if needle.lower() in low:
                failures.append(f"contains text it should not: {needle!r}")
        for pattern in self.expect_matches:
            if not re.search(pattern, output, re.I | re.M):
                failures.append(f"no match for pattern: {pattern!r}")
        return failures


def load_cases(skill: str | None) -> list[Case]:
    if not CASES.is_dir():
        return []
    cases = [Case.load(p) for p in sorted(CASES.glob("*.toml"))]
    return [c for c in cases if skill is None or c.skill == skill]


def emit(cases: list[Case], dest: Path) -> int:
    dest.mkdir(parents=True, exist_ok=True)
    for case in cases:
        body = (
            f"# Eval case: {case.id}\n"
            f"# Skill under test: skills/{case.skill}/SKILL.md\n"
            f"#\n"
            f"# Read the skill above and docs/house-rules.md, then respond to the task.\n"
            f"# Save your response to evals/outputs/{case.id}.txt and run ./evals/run.py\n\n"
            f"{case.prompt}\n"
        )
        (dest / f"{case.id}.txt").write_text(body, encoding="utf-8")
    print(f"wrote {len(cases)} prompt(s) to {dest}")
    print(f"record responses in {OUTPUTS.relative_to(ROOT)}/<case-id>.txt, then re-run without --emit")
    return 0


def check(cases: list[Case], strict: bool) -> int:
    passed = failed = skipped = 0

    for case in cases:
        recording = OUTPUTS / f"{case.id}.txt"
        if not recording.exists():
            skipped += 1
            print(f"SKIP {case.id}  (no recording at evals/outputs/{case.id}.txt)")
            continue

        failures = case.score(recording.read_text(encoding="utf-8"))
        if failures:
            failed += 1
            print(f"FAIL {case.id}  [{case.skill}]")
            for f in failures:
                print(f"       {f}")
            if case.rationale:
                print(f"       why this case exists: {case.rationale}")
        else:
            passed += 1
            print(f"PASS {case.id}  [{case.skill}]")

    print(f"\n{passed} passed, {failed} failed, {skipped} without a recording")

    if failed:
        return 1
    if skipped and strict:
        print("strict mode: every case must have a recording", file=sys.stderr)
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skill", help="only cases for this skill")
    ap.add_argument("--emit", metavar="DIR", type=Path, help="write prompt files instead of scoring")
    ap.add_argument("--strict", action="store_true", help="fail if any case lacks a recording")
    args = ap.parse_args()

    try:
        cases = load_cases(args.skill)
    except ValueError as exc:
        print(f"invalid case: {exc}", file=sys.stderr)
        return 2

    if not cases:
        print("no cases found" + (f" for skill {args.skill!r}" if args.skill else ""))
        return 0 if not args.strict else 1

    OUTPUTS.mkdir(exist_ok=True)
    return emit(cases, args.emit) if args.emit else check(cases, args.strict)


if __name__ == "__main__":
    sys.exit(main())
