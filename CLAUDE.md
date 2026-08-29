# atelier-g — agent entry point

You are working in the repository that defines how this shop builds software.
Read this file first, then the specific documents it points to.

## Before anything else

1. Read [`docs/house-rules.md`](docs/house-rules.md). It is short and it is binding.
2. Identify which skill covers the task at hand (table below). Read that skill in
   full before acting.
3. If no skill covers it, do the work carefully and note in your PR that a skill
   may be missing.

## Skill routing

| The task is… | Read |
|---|---|
| Scoping a request into a plan | `skills/plan-feature/SKILL.md` |
| Writing or changing code against a plan | `skills/implement-change/SKILL.md` |
| Adding, fixing or reasoning about tests | `skills/write-tests/SKILL.md` |
| Reviewing a diff | `skills/review-code/SKILL.md` |
| Preparing a pull request | `skills/ship-pr/SKILL.md` |
| Deciding what to do with an inbound issue | `skills/triage-issue/SKILL.md` |
| Starting a new project or package | `skills/scaffold-project/SKILL.md` |
| Recording an architectural decision | `skills/write-adr/SKILL.md` |

## Working in *this* repository specifically

This repo's product is Markdown. Treat prose with the seriousness you would treat
code.

- `skills/` is the source of truth. **Never edit `.claude/skills/`** — it is
  generated. Edit `skills/` and run `./scripts/sync-harnesses.sh`.
- Every skill must pass `./scripts/validate-skills.py` before commit.
- A behavioural change to a skill requires a case in `evals/cases/`.
- Skills must contain no harness-specific syntax. See
  [ADR-0002](docs/adr/0002-harness-neutral-skills.md).
- Keep skills under ~150 lines. A skill that needs more is two skills, or it needs
  a reference file beside it.

## Style for prose in this repo

- Second person, imperative. "Read the failing test", not "the agent should read".
- Concrete over abstract. Name the file, the command, the failure mode.
- No hedging adverbs, no filler openers. Cut the sentence that only announces the
  next sentence.
- British or American spelling — pick one per file and stay consistent.
- Every rule states what to do when the rule cannot be followed.

## Commands available

```bash
./scripts/validate-skills.py     # structural checks on every skill
./scripts/sync-harnesses.sh      # regenerate .claude/ from skills/
./scripts/new-project.sh NAME --template service-ts|service-py
./evals/run.py                   # run skill eval cases
```

## What not to do here

- Do not add a dependency to this repo. It is Markdown plus a little Python and
  shell, deliberately. Tooling that needs a package manager belongs in a template.
- Do not write a skill that assumes a specific model. Skills describe procedure and
  standards, not prompting tricks.
- Do not let this file grow. It is a router, not a manual.
