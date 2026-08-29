# Roles

A skill says *how to do X well*. A role says *who owns a stage, what they may
decide, and what they hand on*. Roles exist so that the work of understanding a
request, building it, and checking it is done by different parties — the same
context that wrote the code is the worst possible judge of whether it meets the
requirement.

This directory is the source of truth. `scripts/sync-harnesses.sh` projects it
into `.claude/agents/` so each role runs as a genuinely separate agent with its
own context. On a harness without subagents, one agent adopts each role in turn
and must re-read the role charter at every handoff — weaker, but the gates still
hold. See [ADR-0004](../docs/adr/0004-role-based-delivery-pipeline.md).

## The six

| Role | Owns | Appears in |
|---|---|---|
| [`engagement-manager`](engagement-manager/ROLE.md) | Finding out what the project actually is | New projects only |
| [`business-analyst`](business-analyst/ROLE.md) | The specification, the issue set, and final verification | Every pipeline |
| [`tech-lead`](tech-lead/ROLE.md) | Sequencing the work and the quality of what lands | Every pipeline |
| [`principal-engineer`](principal-engineer/ROLE.md) | Application implementation | Every pipeline |
| [`infra-engineer`](infra-engineer/ROLE.md) | CI, deployment, environments, observability | Where infra issues exist |
| [`qa-engineer`](qa-engineer/ROLE.md) | Testing end to end against acceptance criteria | Every pipeline |

## Charter format

```
roles/<kebab-name>/ROLE.md
```

Frontmatter declares `name` (matching the directory), `description` (when to
dispatch this role), and `access`:

- `read-only` — may read, search and run commands, but cannot edit files. Only
  `qa-engineer` holds this, because it is the one role whose entire output is a
  report.
- `read-write` — may edit files and run commands. Every other role needs it: the
  engagement manager writes a brief, the analyst writes specifications and issues,
  the tech lead writes ADRs.

Note honestly what this does and does not buy. `access` stops QA from editing what
it is judging. It does **not** stop the tech lead or the analyst from writing
implementation code — nothing mechanical does. That boundary lives in each
charter's "You may not" section and depends on the role honouring it. If a role
starts implementing what it is meant to review, the pipeline has already failed
and no tool permission will catch it.

`access` is deliberately abstract. The sync script translates it into whatever
each harness calls its tool permissions; the charter itself names no tools, per
[ADR-0002](../docs/adr/0002-harness-neutral-skills.md).

Every charter states, in this order: what the role owns, what it is given, what
it produces, the gate it must pass, what it may decide alone, what it must
escalate, and what it may not do. The last section matters most — a role without
boundaries collapses into "do the whole thing".

## Rules

- A role never grades its own work. The producing role and the verifying role are
  always different.
- A handoff is an artefact, not a conversation. If the next role cannot start from
  the artefact alone, the previous stage is not finished.
- Roles follow [`../docs/house-rules.md`](../docs/house-rules.md) like everyone
  else. A charter may add constraints; it may never relax them.
