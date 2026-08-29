---
name: manage-issues
description: >
  Use when turning a specification into GitHub issues, picking one up, or closing
  one. Covers how an issue is written, how work is labelled and assigned by role,
  and the evidence required before an issue may be closed.
---

# Manage issues

An issue is the unit of work in this shop. It is the contract between the person
who specified something and the person who builds it, and it is the record that
the thing was actually finished.

## Writing an issue

One issue per coherent cluster of acceptance criteria, sized to a pull request
someone can review in one sitting. If it needs more than about 400 lines of real
change, it is two issues.

**Title** — the outcome, in the user's terms, as a statement:
`Signed-in users can save a card at checkout`. Not `Add card model`.

**Body**:

```markdown
## Context
Why this exists. Link the specification. Two sentences.

## Acceptance criteria
Copied verbatim from the specification, with their numbers kept.

  AC3. Given a signed-in user with no saved cards,
       When they complete a payment and tick "save this card",
       Then the card appears in their saved cards on the next checkout.

## Out of scope
What a reasonable person might assume is included and is not.

## Notes
Existing code this touches. Known constraints. Anything the implementer would
otherwise have to rediscover.
```

Criteria are copied, not paraphrased. A paraphrase drifts, and then two documents
disagree about what was asked for.

**Coverage check.** Before handing over an issue set, confirm every acceptance
criterion in the specification appears in exactly one issue. A criterion in no
issue is a feature nobody builds; a criterion in two is a merge conflict.

## Labels

Enough to route the work, and no more:

- `role:engineering` — application implementation
- `role:infra` — CI, deploy, environments, configuration, observability
- `role:qa` — verification work that is its own task
- `blocked` — cannot start; the body says what it waits on
- `needs-info` — the specification is ambiguous here; the analyst owes an answer

Group an issue set under one milestone per delivery cycle. The milestone closes at
user signoff; issues close as they finish.

## Picking one up

Before starting: confirm it is assigned to your role, unblocked, and that its
acceptance criteria are unambiguous. If any criterion could be read two ways, add
`needs-info` and ask — do not choose an interpretation quietly. A wrong guess here
costs a full verification cycle.

Comment on the issue when you start, so two roles do not take the same one.

## Closing

An issue closes when its acceptance criteria are met, reviewed, and verified —
not when the code is written.

Required before closing:

- The pull request is merged, and its body says `Closes #N`
- The tech lead's review findings are resolved
- QA has a PASS for every acceptance criterion in the issue
- Anything found but not fixed is a new issue, linked

Close with a comment naming the evidence: the PR, and the criteria that passed.
`Closes #14 — AC3 and AC4 pass, PR #22, QA report 2026-08-29.` An issue closed
with no trace of why is a record nobody can trust later.

**Never close an issue with an unmet criterion.** If part of it is done and part
is not, split it: close what is genuinely finished, open a new issue carrying the
unmet criteria forward, and link them.

## Reopening

When the analyst's verification finds a criterion unmet, reopen the original issue
rather than filing a fresh one. The history of what was tried belongs with the
requirement. Add a comment stating which criterion failed and what was observed.

## Failure modes

- **The issue that restates the title.** No context, no criteria, no notes — the
  implementer rediscovers everything the analyst already knew.
- **Closing on merge.** Merged is not verified. The PR closing an issue
  automatically is convenient and wrong when QA has not run; reopen it if so.
- **Paraphrased criteria.** The issue and the specification drift, and the
  verification stage cannot tell which is authoritative.
- **The oversized issue.** Twelve criteria in one issue produces a PR nobody can
  review and a partial close nobody notices.
- **Silent interpretation.** Choosing a reading of an ambiguous criterion instead
  of asking. This is the single most expensive habit in the pipeline.
