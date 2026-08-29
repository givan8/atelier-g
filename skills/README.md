# Skill library

Canonical, harness-neutral. This directory is the source of truth; `.claude/` and
any other harness directory are generated from it by
`../scripts/sync-harnesses.sh`.

Each skill is one directory containing `SKILL.md`, plus optional supporting files
that `SKILL.md` links to. Frontmatter declares `name` (equal to the directory name)
and `description` (the triggering conditions, in the words someone would use to
describe their situation).

## Index

| Skill | Trigger |
|---|---|
| `route-request` | **Every request starts here** — which delivery path does it take |
| `manage-issues` | Writing, picking up or closing a GitHub issue |
| `plan-feature` | A request needs scoping before code is written |
| `implement-change` | Writing code against an agreed plan or an understood bug |
| `write-tests` | Adding, repairing or judging test coverage |
| `review-code` | Reviewing a diff, yours or someone else's |
| `ship-pr` | Turning finished work into a mergeable pull request |
| `triage-issue` | An inbound issue or request needs a decision |
| `scaffold-project` | Starting a new service, package or repository |
| `write-adr` | A decision will outlive the conversation that produced it |

## How they fit together

```
                         route-request
                               │
        ┌──────────────┬───────┴────────┬─────────────────┐
        ▼              ▼                ▼                 ▼
     answer      trivial change    enhancement       new project
   (no skill)          │            (BA first)     (engagement first)
                       │                └────────┬────────┘
                       │                         ▼
                       │                   manage-issues
                       │                         │
                       └────────────┬────────────┘
                                    ▼
              plan-feature ──▶ implement-change ──▶ ship-pr
                                    │  ▲               │
                                    ▼  │               ▼
                               write-tests        review-code

              write-adr  ◀──────── (any step that makes a decision)
              scaffold-project ──── stands up a new repository

```

Roles own the stages; skills are what roles use inside them. See
[`../roles/README.md`](../roles/README.md).

See [`../workflows/`](../workflows/) for the end-to-end procedures that sequence
these, and [`../docs/skill-authoring.md`](../docs/skill-authoring.md) to add one.

## Rules

- Under ~150 lines. Longer means it is two skills, or the detail belongs in a
  linked reference file.
- No harness-specific syntax ([ADR-0002](../docs/adr/0002-harness-neutral-skills.md)).
- No duplicated policy — link to [`../docs/house-rules.md`](../docs/house-rules.md).
- Every behavioural change needs a case in [`../evals/cases/`](../evals/cases/).
