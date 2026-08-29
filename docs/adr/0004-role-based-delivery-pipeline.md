# 4. Delivery runs through roles with gates, and a written fast path

- **Status:** Accepted
- **Date:** 2026-08-29

## Context

The first version of this repository was a library of skills. A skill raises the
floor on a task, but nothing decided *which* task was being done, in what order,
or by whom — so a request went straight to implementation. The predictable results
followed: work built on an unstated understanding of the problem, no point at
which the user could correct a misunderstanding cheaply, and verification done by
the same context that wrote the code, which finds nothing because it is checking
its own reasoning.

Agents make this sharper than a human team would. One context that specifies,
builds and verifies is not three parties; it is one party agreeing with itself
three times.

There is an opposing failure. A pipeline applied to everything makes small work
unbearable, and a pipeline people route around is worse than none, because the
bypasses are invisible.

## Decision

Work moves through six roles with explicit gates, defined in `roles/` and
sequenced by `workflows/new-project-delivery.md` and
`workflows/enhancement-delivery.md`.

The roles: `engagement-manager` (new projects only), `business-analyst`,
`tech-lead`, `principal-engineer`, `infra-engineer`, `qa-engineer`.

Three rules make the pipeline mean something:

1. **No role grades its own work.** The producing and verifying roles are always
   different. Only `qa-engineer` is enforced mechanically (`access: read-only`,
   because its whole output is a report); every other separation rests on the
   charter's "You may not" section. That is a real weakness and worth stating: a
   tech lead that writes the code it reviews cannot be stopped by a tool
   permission, only by the charter and by the user noticing.
2. **A handoff is an artefact, not a conversation.** If the next role cannot start
   from the artefact alone, the stage is not finished.
3. **Two gates belong to the user** and cannot be self-served: confirmation of the
   specification, and signoff on delivery.

`skills/route-request/SKILL.md` is the entry point for every request, and offers
two paths that skip the pipeline: answering a question, and a fast path for
trivial changes governed by six written criteria, all of which must hold.

The BA's confirmation artefact is a written specification — acceptance criteria,
interaction descriptions in prose, data shapes — and not a mockup or a prototype.

## Consequences

**Good.** A misunderstanding is caught at the specification gate, where it costs a
paragraph, rather than after implementation, where it costs a cycle. Verification
is genuinely independent. The user gets two defined moments to steer, and knows
where they are. Every stage leaves a written artefact, so a fresh session — or a
different model — can pick the work up mid-flight.

**Bad.** Latency. Even a modest feature now passes through specification,
confirmation, sequencing, implementation, QA and acceptance, and the two user
gates are as slow as the user is. Handoff artefacts are real work that produces no
running code. Six roles cost more tokens than one.

**The real risk** is the fast path widening under pressure until the pipeline is
decorative. The six criteria are written as a checklist, with an explicit
instruction that they may not be stretched and that uncertainty means the pipeline
— because the alternative, judgement in the moment, always resolves toward speed.

**Accepted cost.** Small work is slower than it needs to be, in exchange for large
work being correct. We chose the fast path over "everything through the analyst"
specifically so that the pipeline stays credible for the work that needs it.

## Alternatives considered

**Skills only, no roles.** The status quo before this. Rejected: nothing decided
what was being built or checked that it was, and self-verification is not
verification.

**Every request through the full pipeline, no fast path.** Maximum consistency and
traceability. Rejected: a typo fix requiring a specification, an issue and a QA
report trains people to bypass the whole thing, and an invisible bypass is worse
than a documented exception.

**One agent adopting each role in sequence.** Cheaper and simpler. Rejected as the
default: the independence that makes review and QA worth anything comes from a
separate context. It remains the fallback on harnesses without subagents, and the
charters are written so the gates still hold when it is used.

**A prototype at the confirmation gate.** A clickable mock is more convincing than
prose. Rejected: it is convincing about the wrong things — it invites feedback on
layout rather than on whether the acceptance criteria are right, it cannot be
diffed in review, and a prototype that exists tends to become the architecture.
Prose that states Given/When/Then can be argued with precisely.
