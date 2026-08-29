---
name: review-code
description: >
  Use when reviewing a diff, pull request or patch — someone else's or your own
  before shipping. Covers what to look for, in what order, and how to write
  findings that get acted on.
---

# Review code

A review's job is to catch what tests cannot: wrong intent, hidden cost, and the
decision nobody wrote down. It is not to enforce style — a linter does that, and if
it does not, fix the linter.

## Order of passes

Do these in order. Stop and report if an earlier pass finds something fatal; there
is no point commenting on naming in a change that solves the wrong problem.

### 1. Intent

Does this change do what it claims? Read the PR body, then the diff, and check they
describe the same thing. A diff that does more than the description is the single
most common source of surprise regressions.

Ask: was this the problem worth solving? If the answer is no, say so now, kindly
and early.

### 2. Correctness

- Walk the happy path with a concrete input, in your head, line by line.
- Then walk it with: empty, null/None, zero, negative, very large, concurrent.
- Every error path — where does it go, what does the caller see?
- Off-by-one, inclusive/exclusive bounds, and anything involving a timezone.
- Concurrency: shared mutable state, ordering assumptions, partial failure.

### 3. Consequences

The things that do not show up in the diff:

- Does this break an existing caller? Search for usages, do not assume.
- Migration and rollback: can this be reverted after it has run once?
- Does it change performance characteristics at realistic data volume — an N+1, an
  unindexed query, an unbounded collection held in memory?
- Security: input validation at the boundary, authorisation checks, anything
  logged that should not be.

### 4. Tests

- Is the new behaviour actually asserted, or only executed?
- For a bug fix: would this test have failed before the change? If you cannot
  tell, ask for the failing output.
- Was any existing test weakened? Look specifically for loosened assertions,
  added retries, and new skips.

### 5. Legibility

- Will this read clearly to someone in six months with no context?
- Names: does each one say what the thing is, and is it still true after the
  change?
- Comments explain *why*; delete ones that narrate *what*.
- Is there a decision here that needs an [ADR](../write-adr/SKILL.md)? New
  pattern, new dependency, new data shape — usually yes.

### 6. Hygiene

Debug output, commented-out code, `TODO` without an issue, stray files, secrets or
real data in fixtures. Quick pass, but do it — this is what leaks.

## Writing findings

State the problem, the consequence, and a suggestion. Findings without a
consequence get argued with; findings without a suggestion get deferred.

> `parseConfig` swallows the error at line 42, so a malformed config file starts
> the service with defaults instead of failing. Suggest rethrowing with the file
> path attached.

Label severity so the author can triage:

- **Blocking** — must change before merge. Correctness, security, data loss, a
  broken contract.
- **Should fix** — merge is possible, but this will cost someone later.
- **Note** — an observation, a preference, a thing worth knowing. Explicitly not
  a request.

Rules for tone: review the code, never the author. Ask when you are unsure rather
than asserting — "what happens if this is called twice?" is better than "this is
not idempotent" when you have not checked. Say what is good, briefly and
specifically, when it is; a review of only faults trains people to dread reviews.
Do not repeat a point in three places.

## Approving

Approve when the blocking findings are resolved and you would be comfortable being
the one who gets paged for this change. Not when you have run out of things to say.

If the change is outside your competence, say that instead of approving. "I cannot
assess the crypto here, someone else should look" is a useful review.

## Reviewing your own diff before shipping

The same passes, with one addition: read the diff in the PR view, not the editor.
Different presentation catches different mistakes — leftover debugging, an
accidentally staged file, a hunk you meant to drop.

## Failure modes

- **Style policing.** If it can be automated, automate it and stop mentioning it.
- **Rubber-stamping length.** Large diffs get less attention exactly when they
  need more. Ask for a split instead.
- **Nitpicks blocking merge.** Label them as notes and let them go.
- **Assuming the tests cover it.** Read what they actually assert.
- **Reviewing an agent's PR more loosely.** Same standard, per
  [house rule 8](../../docs/house-rules.md).
