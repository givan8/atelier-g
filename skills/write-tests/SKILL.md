---
name: write-tests
description: >
  Use when adding tests for new behaviour, writing a reproduction for a bug,
  repairing a failing or flaky test, or judging whether existing coverage is
  adequate. Language-agnostic; defers runner and layout to the project template.
---

# Write tests

A good test fails for exactly one reason, and its name tells you what that reason
is. Coverage percentage is not the goal — catching the regression is.

## What to test

Test **behaviour at the boundary of a unit**, not its internals. If a test breaks
when you rename a private method, it was testing the wrong thing.

Priority order when time is limited:

1. The path the user actually takes
2. The error paths — these are where untested code hides
3. Boundaries: empty, one, many, maximum, just over maximum
4. The specific bug you are fixing

Do not test: framework behaviour, language semantics, generated code, or that a
mock was called with the arguments you just passed it.

## Structure

Three phases, visibly separated — arrange, act, assert. One behaviour per test. If
you need "and" to describe what a test checks, it is two tests.

Name the test after the behaviour, in a sentence, from the caller's point of view:

```
✗ test_user_2
✓ rejects a signup when the email is already registered
```

The name is documentation. Someone reading a CI failure log should understand what
broke without opening the file.

## Assertions

- Assert the specific thing, not that "something happened". `assert result.status
  == "rejected"` beats `assert result is not None`.
- Assert on values, not on call counts, wherever you have the choice.
- One conceptual assertion per test. Several `assert` lines checking one outcome
  is fine; checking three unrelated outcomes is not.
- Include a message on assertions whose failure would be cryptic.

## Test data

- Build the minimum object the test needs. A fixture with twenty fields where the
  test reads two is noise that hides the two that matter.
- Make the significant value obvious: `email="duplicate@example.test"` says what
  the test is about; `email="a@b.c"` does not.
- Never use real customer data, real keys, or real endpoints. Ever.
- Prefer a factory function with defaults over a shared mutable fixture. Shared
  mutable state between tests is how you get order-dependent suites.

## Mocking

Mock at the edges of your system — network, clock, filesystem, third-party
services — and nowhere else.

Every mock is an assumption about how a real thing behaves, and it is not checked.
A suite that mocks everything proves the mocks agree with each other. If you find
yourself mocking your own code, the design is probably too coupled to test; fix
that instead.

Freeze time explicitly rather than sleeping. `sleep` in a test is a flake waiting
for a slow CI runner.

## Fixing a failing test

Work out which of these it is before you touch anything:

- **The code is wrong** → fix the code.
- **The test encoded behaviour you deliberately changed** → update the test, and
  say so in the commit message. This is legitimate and must be visible.
- **The test is flaky** → find the source of nondeterminism (time, ordering,
  network, shared state, unseeded randomness) and remove it.

Never: add a retry, loosen an assertion, or mark it skipped to get green. A skipped
test is a lie that passes CI. If you truly must disable one, it needs an issue
number and a date in the comment.

## Bug reproductions

The order matters. Write the test, run it, **watch it fail**, then fix the code.
A test written after the fix proves nothing — you have no evidence it would have
caught the bug.

## Failure modes

- **Testing the implementation.** Brittle, breaks on every refactor, catches
  nothing.
- **The mega-test.** Fifty lines exercising a whole workflow; when it fails you
  learn only that something, somewhere, is wrong.
- **Coverage theatre.** Calling every function with no meaningful assertions.
- **Snapshot dumping.** A snapshot no one reads is a rubber stamp; it gets
  regenerated on failure without thought.
- **Nondeterminism.** Real clocks, real network, unseeded random, ordering
  assumptions on unordered collections.

## Project specifics

Runner, directory layout, naming convention and coverage thresholds are per
language and live with the project — see `templates/service-ts/CONVENTIONS.md` or
`templates/service-py/CONVENTIONS.md`. The principles above do not change between
languages; the mechanics do.
