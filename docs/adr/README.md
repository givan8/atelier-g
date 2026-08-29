# Architecture decision records

A decision gets an ADR when it is expensive to reverse, when a future reader would
otherwise ask "why on earth is it like this", or when a reasonable person would
have chosen differently.

Not every choice needs one. Picking a variable name does not. Picking a database
does.

## Format

One file per decision: `NNNN-short-title-in-kebab-case.md`, numbered sequentially,
never renumbered. Use [`../../templates/_shared/adr-template.md`](../../templates/_shared/adr-template.md).

Sections: **Status**, **Context**, **Decision**, **Consequences**, **Alternatives
considered**. Consequences must include the bad ones — an ADR that lists only
upsides is marketing, not a record.

## Status lifecycle

`Proposed` → `Accepted` → (later) `Superseded by ADR-NNNN` or `Deprecated`.

Never edit an accepted ADR's decision to reflect a change of mind. Write a new ADR
that supersedes it and link both ways. The wrong turns are the valuable part of the
record.

## Index

| # | Title | Status |
|---|---|---|
| [0001](0001-record-architecture-decisions.md) | Record architecture decisions | Accepted |
| [0002](0002-harness-neutral-skills.md) | Skills are harness-neutral Markdown | Accepted |
| [0003](0003-generated-harness-directories.md) | Harness directories are generated, not authored | Accepted |
| [0004](0004-role-based-delivery-pipeline.md) | Delivery runs through roles with gates, and a written fast path | Accepted |
| [0005](0005-github-issues-as-the-unit-of-work.md) | GitHub issues are the unit of work, and close only with evidence | Accepted |
