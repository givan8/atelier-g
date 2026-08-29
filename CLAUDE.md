# atelier-g — agent entry point

You are working in the repository that defines how this shop builds software.

## Start here, every time

**Read [`skills/route-request/SKILL.md`](skills/route-request/SKILL.md) and route
the request before doing anything else.** It decides between four paths: answer a
question, fast-path a trivial change, run the enhancement pipeline, or run the new
project pipeline. Say which path you took.

Then read [`docs/house-rules.md`](docs/house-rules.md). It is short and binding,
and it applies to every role and every path.

## The pipelines

| The request is | Workflow | First role |
|---|---|---|
| A new product or service | [`workflows/new-project-delivery.md`](workflows/new-project-delivery.md) | `engagement-manager` |
| A change to something that exists | [`workflows/enhancement-delivery.md`](workflows/enhancement-delivery.md) | `business-analyst` |
| One issue inside either of those | [`workflows/issue-to-merge.md`](workflows/issue-to-merge.md) | the assigned role |

Roles are defined in [`roles/`](roles/README.md) and run as separate agents:
`engagement-manager`, `business-analyst`, `tech-lead`, `principal-engineer`,
`infra-engineer`, `qa-engineer`. No role grades its own work.

## Skills

Roles use these; so does the fast path.

| The task is | Read |
|---|---|
| Routing any incoming request | `skills/route-request/SKILL.md` |
| Writing, picking up or closing an issue | `skills/manage-issues/SKILL.md` |
| Scoping a request into a plan | `skills/plan-feature/SKILL.md` |
| Writing or changing code | `skills/implement-change/SKILL.md` |
| Adding or fixing tests | `skills/write-tests/SKILL.md` |
| Reviewing a diff | `skills/review-code/SKILL.md` |
| Preparing a pull request | `skills/ship-pr/SKILL.md` |
| Deciding what to do with an inbound issue | `skills/triage-issue/SKILL.md` |
| Starting a new project or package | `skills/scaffold-project/SKILL.md` |
| Recording an architectural decision | `skills/write-adr/SKILL.md` |

## Working in *this* repository specifically

This repo's product is Markdown. Treat prose with the seriousness you would treat
code.

- `skills/` and `roles/` are the source of truth. **Never edit `.claude/`** — all
  of it is generated. Edit the source and run `./scripts/sync-harnesses.sh`.
- Everything must pass `./scripts/validate.py` before commit.
- A behavioural change to a skill or role requires a case in `evals/cases/`.
- No harness-specific syntax in `skills/` or `roles/`. Tool permissions are
  expressed as `access:` and translated by the sync script. See
  [ADR-0002](docs/adr/0002-harness-neutral-skills.md).
- Keep skills and charters under ~150 lines. Longer means it is two of them, or
  the detail belongs in a linked reference file.

## Style for prose in this repo

- Second person, imperative. "Read the failing test", not "the agent should".
- Concrete over abstract. Name the file, the command, the failure mode.
- No hedging adverbs, no filler openers. Cut the sentence that only announces the
  next sentence.
- Every rule states what to do when the rule cannot be followed.
- Every role charter ends with what that role may **not** do.

## Commands

```bash
./scripts/validate.py            # structure of every skill and role
./scripts/sync-harnesses.sh      # regenerate .claude/ from skills/ and roles/
./scripts/new-project.sh NAME --template service-ts|service-py
./evals/run.py                   # score recorded eval responses
```

## What not to do here

- Do not add a dependency. This repo is Markdown plus a little Python and shell,
  deliberately. Tooling that needs a package manager belongs in a template.
- Do not write a skill or charter that assumes a specific model.
- Do not let this file grow. It is a router, not a manual.
