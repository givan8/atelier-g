# 5. GitHub issues are the unit of work, and close only with evidence

- **Status:** Accepted
- **Date:** 2026-08-29

## Context

The delivery pipeline in [ADR-0004](0004-role-based-delivery-pipeline.md) hands
work from an analyst to implementing roles and back to a verifier. Something has
to carry the requirement across those handoffs, survive the end of a session, and
still be readable when the work is questioned months later.

Agents have no memory between sessions. Whatever is not written into a durable,
addressable place does not exist for the next role — and a plan held in a
conversation is gone the moment the conversation ends.

Half-finished work is the specific danger. An issue that is closed when a pull
request merges, before anyone verified the acceptance criteria, produces a
backlog that reads as complete and a product that is not.

## Decision

A GitHub issue is the unit of work. `skills/manage-issues/SKILL.md` governs how
issues are written, labelled, picked up and closed.

- The analyst cuts one issue per coherent cluster of acceptance criteria, each
  sized to a reviewable pull request, with criteria **copied verbatim** from the
  specification rather than paraphrased.
- Every acceptance criterion appears in exactly one issue. The analyst checks
  coverage before handing over.
- Labels route the work: `role:engineering`, `role:infra`, `role:qa`, plus
  `blocked` and `needs-info`. One milestone per delivery cycle.
- An issue closes only when its criteria are **met, reviewed and verified** — a
  merged PR, resolved review findings, and a QA PASS for each criterion — and the
  closing comment names that evidence.
- An issue with an unmet criterion is never closed. It is split: close what is
  finished, open a linked issue carrying the rest.
- Verification failures reopen the original issue rather than filing a new one, so
  the history of what was tried stays with the requirement.

## Consequences

**Good.** State lives outside any session, so work survives a lost context, a new
model, or a week's gap. The trail from requirement to evidence is reconstructable
by anyone with the repository. Labels let the tech lead assign without a
conversation. Reopening rather than refiling keeps the argument in one place.

**Bad.** Real overhead: a specification of eight criteria becomes several issues
that must be written well, and badly written issues are worse than none because
they are trusted. Copying criteria verbatim duplicates text between the
specification and the issues, and duplication drifts — mitigated only by the rule
that the specification is authoritative.

**The friction that matters** is the close rule. `Closes #N` in a merged PR shuts
the issue automatically, before QA has run. The pipeline requires reopening it in
that case, which is easy to forget and produces exactly the false-complete backlog
this decision exists to prevent. If that turns out to happen often, the fix is to
stop using the auto-closing keyword rather than to relax the rule.

## Alternatives considered

**A task list in the repository, as a Markdown file.** Simple, diffable, no API.
Rejected: it does not support assignment, labels or per-item discussion, and every
role editing one file produces constant conflicts.

**A project management tool.** Better reporting and planning views. Rejected: it
puts the record somewhere an agent with only the repository cannot reach, and adds
a credential and an integration to every session.

**Issues, but closed on merge.** Conventional, and much less friction. Rejected:
merged is not verified. Closing at merge is precisely how a backlog comes to
describe work that was written but never checked against what was asked for.

**Tracking work only in the conversation.** Rejected outright: it does not survive
the session, which is the one thing the record has to do.
