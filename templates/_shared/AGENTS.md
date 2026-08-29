# AGENTS.md — {{PROJECT_NAME}}

This project follows the atelier-g house standard:
https://github.com/givan8/atelier-g

## Before you change anything here

1. **Route the request first** with `atelier-g/skills/route-request/SKILL.md`.
   Anything that changes behaviour here and is not trivial runs the enhancement
   pipeline: business analyst, then implementation, then QA, then verification and
   your signoff. Say which path you took.
2. Read `atelier-g/docs/house-rules.md`. It is binding.
3. Read the skill that covers your task from `atelier-g/skills/`:

   | Task | Skill |
   |---|---|
   | Routing any request | `route-request` |
   | Writing or closing an issue | `manage-issues` |
   | Scoping a request | `plan-feature` |
   | Writing code | `implement-change` |
   | Tests | `write-tests` |
   | Reviewing a diff | `review-code` |
   | Opening a PR | `ship-pr` |
   | A decision worth keeping | `write-adr` |

4. Read this project's `README.md` and `docs/adr/` before designing anything. The
   ADRs explain why this project is shaped the way it is; changing something an
   ADR decided requires a new ADR, not a quiet edit.

## This project specifically

<!-- Replace this section with what is true here. Delete it if there is nothing
     project-specific — an empty section is better than an aspirational one. -->

- **What it does:** TODO
- **Run locally:** see README
- **Tests:** see README
- **Things that will surprise you:** TODO

## Non-negotiables

- Branch, never commit to the default branch.
- New behaviour arrives with a test. Bug fixes arrive with a test that failed
  first.
- No secrets in the repository. Configuration comes from the environment;
  `.env.example` lists what is needed.
- Stop and ask a human for: data deletion, irreversible migrations, auth, crypto,
  or payments.
