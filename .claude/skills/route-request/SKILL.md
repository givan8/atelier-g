---
name: route-request
description: >
  Use at the start of every request, before doing anything else. Decides whether
  the request is a question, a trivial change, an enhancement to an existing
  project, or a new project — and starts the right pipeline. The entry point for
  all work.
---

<!-- GENERATED FROM skills/route-request/SKILL.md — DO NOT EDIT. Run ./scripts/sync-harnesses.sh -->

# Route a request

Every request starts here. Your job is one decision: which of four paths this
request takes. Make it explicitly, say which path you chose, and start it.

Getting this wrong is expensive in both directions. A new product built without an
engagement stage is built on a guess. A typo fix sent through six roles will make
the user stop using the pipeline.

## The four paths

### 1. Answer — no pipeline

The request asks for information, not a change: explaining code, finding
something, comparing options, reading a file, research, a recommendation.

Answer it. Do not create an issue. If the answer turns out to require a change,
route that change on its own.

### 2. Trivial change — fast path

Straight to [`implement-change`](../implement-change/SKILL.md) and
[`ship-pr`](../ship-pr/SKILL.md), no roles, no issue set.

**A change qualifies only if every one of these is true:**

1. It changes no behaviour a user or caller can observe — *or* it fixes a defect
   whose cause you have already identified and can name.
2. It is confined to one file, or a few lines across a small number of files.
3. It needs no new interface, dependency, schema, configuration or environment
   variable.
4. Existing tests cover it, or one obvious test is enough.
5. A single revert undoes it completely.
6. It touches none of: authentication, authorisation, cryptography, payments,
   data migration, data deletion, access control.

All six, or it is not trivial. **You may not stretch this bar**, and you may not
reason that a change is "basically" trivial. When you are unsure, it is not — take
path 3. The bar is written down precisely so that time pressure cannot widen it.

Say which path you took and why, in one line, so the user can correct you cheaply:
*"Fast-pathing this — one file, no observable behaviour change, covered by the
existing test."*

### 3. Enhancement — existing project

The request changes behaviour in a codebase that already exists, and does not
qualify as trivial.

Start [`../../workflows/enhancement-delivery.md`](../../../workflows/enhancement-delivery.md).
Business analyst first. No engagement manager — the project's purpose is already
established; what is missing is a precise statement of this change.

### 4. New project — no codebase yet

A new product, service, or application. Nothing exists, or what exists is
unrelated to what is being asked for.

Start [`../../workflows/new-project-delivery.md`](../../../workflows/new-project-delivery.md).
Engagement manager first: what the project actually is has to be established
before anyone specifies or designs it.

## How to decide

Ask in this order, and stop at the first yes:

1. **Is anything being changed?** No → path 1.
2. **Is there an existing codebase this belongs to?** No → path 4.
3. **Does it meet all six trivial criteria?** Yes → path 2.
4. Otherwise → path 3.

Two cases that look ambiguous and are not:

- **"Add X to project Y" where Y exists.** Enhancement, however large. A new
  repository may still come out of it — that is the analyst's finding, not an
  intake decision.
- **"Rewrite Y from scratch."** New project. The problem needs re-establishing,
  even though a codebase exists.

## Failure modes

- **Fast-pathing under pressure.** The most common failure. A change that is
  urgent is not thereby trivial — urgency is the reason the bar is written down.
- **Routing a question into the pipeline.** Producing a specification for
  "how does auth work here" wastes the user's time and trains them to bypass you.
- **Skipping engagement because the user sounds certain.** A confident sentence
  describing a solution is exactly the case the engagement stage exists for.
- **Deciding silently.** Always say which path you took. A wrong route is cheap to
  correct in the first message and expensive to correct three stages later.

## When the user overrides

If the user says to skip a stage, do it, and say once what the skipped stage would
have caught. Do not repeat the point.
