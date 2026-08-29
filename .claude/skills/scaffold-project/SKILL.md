---
name: scaffold-project
description: >
  Use when starting a new service, package or repository so it begins with the
  house standard rather than drifting into it. Covers what a new project must
  have on day one and what it must not have.
---

<!-- GENERATED FROM skills/scaffold-project/SKILL.md — DO NOT EDIT. Run ./scripts/sync-harnesses.sh -->

# Scaffold a project

A new project is the cheapest moment to get the standard right and the most
expensive moment to skip it. Everything omitted on day one gets added later at ten
times the cost, or never.

## Procedure

### 1. Justify the new repository

A new repository is a permanent maintenance obligation: CI, dependencies, secrets,
access, releases, and a README someone has to keep true. Before creating one, check
that this cannot be a package or module inside an existing project.

Good reasons: a different deployment lifecycle, a different security boundary, a
different team owning it. Bad reasons: a different language, a feeling of
tidiness.

### 2. Generate from a template

```bash
./scripts/new-project.sh <name> --template service-ts   # or service-py
```

The template supplies the tooling baseline, `_shared/` supplies the house
standard, and `AGENTS.md` in the generated repo points back at atelier-g so agents
working there pick up these skills.

If no template fits, use the closest one and open an issue for the gap. Do not
hand-roll a new project from scratch — that is how conventions diverge.

### 3. Name it

Lowercase, hyphenated, no abbreviations a new person would have to look up. Name
it after what it does, not what it is built with. `billing-webhooks`, not
`svc-bwh-node`.

### 4. Fill in the parts a template cannot

- **README** — what this is, who it is for, how to run it locally, how to run the
  tests, how to deploy. A README saying "TODO" on day one says "TODO" forever.
- **The first ADR** — record why this project exists and the shape chosen. This is
  the decision most worth writing down and the one most often skipped.
- **Ownership** — who is responsible when it breaks, in `CODEOWNERS`.

### 5. Prove it works before writing features

Do not accept a scaffold you have not run:

- [ ] Install from a clean clone, following the README exactly
- [ ] Tests run and pass — including the one placeholder test
- [ ] Lint and type check pass
- [ ] The service starts locally and answers a health check
- [ ] CI passes on the first commit

A scaffold whose CI has never been green is not a scaffold, it is a liability.

### 6. Commit as one atomic change

`chore: scaffold <name> from template <template>`. Do not mix scaffold and first
feature — a reviewer needs to be able to skip the generated part.

## What every project has on day one

- README that is true
- Tests that run with one command, and one real test
- Lint and format config, enforced in CI
- CI on every push and PR
- `.env.example`, and secrets loaded from the environment only
- `AGENTS.md` and `CLAUDE.md` pointing back at atelier-g
- A licence, or an explicit private marker
- Dependency lock file, committed

## What it does not have on day one

Resist all of this until something actually needs it:

- Abstraction layers with one implementation
- A plugin system, a config framework, an internal DSL
- Multiple environments before there is one working one
- A database before there is state worth storing
- A microservice split before the monolith hurts

Per [house rule 5](../../../docs/house-rules.md): boring by default. Structure added
speculatively is structure everyone pays for and nobody uses.

## Failure modes

- **Copying the last project.** You inherit its accidents and its outdated
  dependencies. Use the template; fix the template if it is wrong.
- **Skipping CI "for now".** The first red build lands three weeks of changes
  later and nobody knows which one broke it.
- **The aspirational README.** Documents what the project will do. Document what
  it does.
- **Template drift.** When you fix something in a generated project that was wrong
  in the template, fix the template too, in the same PR if you can.
