# 1. Record architecture decisions

- **Status:** Accepted
- **Date:** 2026-08-29

## Context

Work in this shop is done largely by agents, which have no memory between sessions,
and by humans, who have unreliable memory across months. Both will encounter a
design and need to know whether it was reasoned or accidental. Without a record,
every past decision looks arbitrary, and arbitrary decisions get reversed by
whoever is least aware of the constraint that produced them.

Chat transcripts are not a record. They are unsearchable in practice, they are not
versioned with the code, and they contain ten discarded ideas for every one that
was kept.

## Decision

We record architecturally significant decisions as ADRs in `docs/adr/`, using the
format described in [`README.md`](README.md).

A decision is architecturally significant if reversing it would take more than a
day, if it constrains future choices, or if it is surprising.

Agents are expected to write ADRs as part of their work, not to have one written
for them afterwards. The `write-adr` skill covers the procedure.

## Consequences

**Good.** New contributors — human or model — can reconstruct the reasoning behind
the codebase from the repository alone. Debates that have already been had do not
get re-run. The cost of writing is paid at the moment when the reasoning is still
in working memory, which is the only time it is cheap.

**Bad.** ADRs rot if the discipline lapses; a half-maintained set is worse than
none because it is trusted and wrong. There is a standing temptation to write ADRs
for trivia, which dilutes the set. And writing one is friction at exactly the
moment someone wants to move on to the next thing.

**Mitigation.** The `review-code` skill checks whether a change contains a decision
that should have been recorded. The bar — expensive to reverse, or surprising — is
stated in one place and referenced everywhere else.

## Alternatives considered

**Nothing.** Rely on code comments and PR descriptions. Rejected: PR descriptions
are not discoverable six months later, and comments explain lines rather than
designs.

**A wiki.** Rejected: it drifts from the code, it is not reviewed, and it is not
available to an agent that has only cloned the repository.

**Design docs per project.** Rejected as the primary mechanism — they describe an
intended future rather than a decision made, and they are rarely updated once the
work starts. They remain useful as an input to an ADR.
