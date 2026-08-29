---
name: plan-feature
description: >
  Use when a request needs scoping before code is written — a feature, a
  refactor, a migration, or anything where the shape of the work is not obvious.
  Produces a plan someone else could execute. Use before implement-change, not
  instead of it.
---

# Plan a feature

A good plan is one another person could execute without asking you a question, and
short enough that they will actually read it.

## Procedure

### 1. Restate the request as an outcome

Write one sentence describing what will be true when this is done, in the user's
terms, not the system's. "A user can undo the last three actions" — not "add an
undo stack".

If you cannot write that sentence, you do not understand the request yet. Ask.

### 2. Read the code before designing

Find and read the code this will touch. Specifically:

- The entry point where the new behaviour is triggered
- The nearest existing feature that does something structurally similar
- The tests around both

Copying the shape of the nearest analogous feature is usually right. If you are
about to introduce a pattern this codebase does not already use, that is an
[ADR](../write-adr/SKILL.md), not a detail.

### 3. State the constraints you found

List what actually limits the design: existing schemas, public interfaces you
cannot break, performance characteristics, things the tests pin down. This is the
part that turns a generic plan into a correct one, and it is the part most often
skipped.

### 4. Cut the scope

Name explicitly what is **not** in this change. Every plan has an edge, and the
edge is where disagreements live. Push everything you can into a follow-up.

Prefer a plan that ships a thin end-to-end path over one that builds a complete
layer. A working slice reveals wrong assumptions; a finished layer hides them.

### 5. Break it into reviewable steps

Each step is a commit or a PR that leaves the repository working. Number them.
For each: what changes, what test proves it, roughly how big.

If a step cannot be described in two sentences, split it.

### 6. Name the risks

For each, say what you will do about it:

- What might not work — and how you will find out early
- What could break for existing users — and what test covers it
- What is irreversible — see the escalation list in
  [house rules](../../docs/house-rules.md)

### 7. Get agreement before building

Present the plan. Ask one question: "anything wrong before I start?" Then stop and
wait. A plan built on a misunderstanding is more expensive than no plan, because it
is convincing.

## Output shape

```markdown
## Outcome
One sentence.

## Constraints found
- …

## Not doing
- …

## Steps
1. … (test: …)
2. … (test: …)

## Risks
- Risk → mitigation

## Open questions
- …
```

Keep it under a page. If it is longer, the scope is too big.

## Failure modes

- **Planning without reading.** A plan written from the request alone will invent
  interfaces that do not exist. Read first, always.
- **Boiling the ocean.** If your plan has more than about six steps, cut it and
  plan the first half properly.
- **Fake questions.** Do not list open questions you can answer by reading the
  code. Go read it.
- **Hidden decisions.** If a step embeds a choice a reasonable person would make
  differently, surface it as a question, not as a step.
- **Planning past the unknown.** When step 3 depends on what you learn in step 2,
  say so and plan to replan.

## When this does not apply

- **A one-line fix with an obvious cause.** Just do it, with a test.
- **A bug with no clear cause.** Reproduce it and find the cause first; planning a
  fix you cannot yet name is guessing.
- **An inbound issue that has not been accepted.** Use
  [`triage-issue`](../triage-issue/SKILL.md) first.
