---
name: write-adr
description: >
  Use when a decision will outlive the conversation that produced it — a new
  dependency, a data model, a pattern the codebase does not already use, or any
  choice that is expensive to reverse. Also use when reading an ADR to decide
  whether it still holds.
---

# Write an architecture decision record

An ADR captures why, at a particular moment with particular constraints, this
choice was made. Its readers are people — and agents — who will otherwise assume
the choice was arbitrary and undo it.

## When one is needed

Write an ADR if **any** of these are true:

- Reversing the decision would take more than a day
- It constrains future choices (a schema, a public interface, a dependency)
- A competent person would plausibly have chosen differently
- It is surprising, and a reader would ask "why on earth is it like this"
- It adds a dependency, a service, or a pattern the codebase does not already use

Do not write one for: naming, formatting, anything a linter enforces, or a choice
that can be reversed in an afternoon.

Uncertain? Ask whether you would want to read this in a year. If yes, write it.

## The format

Use [`templates/_shared/adr-template.md`](../../templates/_shared/adr-template.md).
File as `docs/adr/NNNN-kebab-case-title.md`, numbered sequentially, never
renumbered.

### Context

The situation and the constraints, written so a stranger understands the pressure
you were under. Include the constraints that were real at the time even if they
later disappear — that is precisely what makes the record useful later.

Facts, not justification. If this section argues for the decision, you are writing
the wrong section.

### Decision

What was chosen, in the active voice and the present tense: "We store timestamps as
UTC epoch milliseconds." Specific enough that someone can tell whether the code
follows it.

### Consequences

What becomes true — good and bad. **An ADR that lists only upsides is not credible
and will not be trusted.** State plainly what this makes harder, what it commits
us to maintaining, and what you would need to see to reconsider.

### Alternatives considered

Each real alternative, with the reason it was not chosen. This is the section that
stops the same debate being re-run in eighteen months. "We did not consider X"
is itself worth recording.

## Writing it well

- Write it at the moment of decision. The reasoning is available for about an hour
  and then it is gone.
- Present tense for the decision, past tense for the context.
- Name the trade-off you accepted, explicitly. Every decision has one; an ADR that
  cannot name it has not identified the real choice.
- Keep it under a page. Long ADRs go unread, which defeats the purpose.
- No hedging. "We chose Postgres" — not "it was felt that Postgres might be
  suitable".
- Link the PR, the issue, or the benchmark that informed it.

## Changing your mind

Never edit an accepted ADR's decision. Write a new one that supersedes it:

- New ADR: `Supersedes ADR-0007`, with what changed and why.
- Old ADR: status becomes `Superseded by ADR-0012`. Leave the body untouched.

The wrong turns are the valuable part of the record. Rewriting history to look
correct destroys exactly the information a future reader needs.

## Reading an ADR later

When you find one that seems to be blocking sensible work, check whether the
*context* still holds before concluding the decision is wrong. Decisions usually
expire because their constraints did, not because they were mistaken. If the
constraints are gone, supersede it — with a record, not silently.

## Failure modes

- **The retrospective ADR.** Written weeks later, it documents a rationalisation
  rather than a decision.
- **The one-sided ADR.** All benefits, no costs. Nobody believes it.
- **The ADR for everything.** Diluting the set until nobody reads any of them.
- **Editing the past.** Updating an old ADR to match current practice, erasing the
  reason the change happened.
- **Deciding in chat.** A decision that exists only in a conversation will be made
  again, differently, by whoever is in the room next time.
