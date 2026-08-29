---
name: implement-change
description: >
  Use when writing or modifying code against an agreed plan or a well-understood
  bug. Covers the working loop — branch, small commits, tests alongside, verify
  before claiming done. The default skill for hands-on-keyboard work.
---

<!-- GENERATED FROM skills/implement-change/SKILL.md — DO NOT EDIT. Run ./scripts/sync-harnesses.sh -->

# Implement a change

Good work here is boring: small commits that each leave the repository working, and
a claim of "done" that is true.

## Before the first edit

- Confirm you have a plan ([`plan-feature`](../plan-feature/SKILL.md)) or that the
  change is small and the cause is understood.
- Branch. Never commit to the default branch.
  `git switch -c <type>/<short-description>` — type is `feat`, `fix`, `chore`,
  `docs`, or `refactor`.
- Run the existing test suite and note what already fails. You are not responsible
  for pre-existing failures, but you must know about them or you will blame
  yourself for them later.

## The loop

Repeat per step of the plan:

1. **Write the test first when you can.** For a bug, write the test that
   reproduces it and watch it fail — a bug fix without a failing test first is a
   guess that happens to compile.
2. **Make the smallest change that passes.** Resist doing the next step at the
   same time.
3. **Run the tests.** All of them, not just the one you wrote.
4. **Run lint and type checks.** Fix them now; they do not get cheaper.
5. **Commit.** One logical change per commit, message in the imperative:
   `fix: reject empty tenant id in signup`. Body explains why if it is not obvious.

## Working with existing code

- Match the surrounding style even where you would have chosen differently. A file
  with two conventions is worse than a file with one convention you dislike.
- Change the smallest surface that achieves the outcome. Widening a public
  interface is a decision; narrowing one is a breaking change.
- When you must touch something unrelated, do it in a separate commit so the
  reviewer can skip it.
- Delete code you have made unreachable. Do not comment it out — git remembers.

## Errors and edge cases

Follow [house rule 6](../../../docs/house-rules.md): fail loudly. Concretely:

- No empty catch blocks. If an error is genuinely expected and safe, the catch has
  a comment saying why.
- Validate at the boundary — where data enters the system — not repeatedly inside.
- Every new error path gets a test. Error paths are where untested code hides.
- Preserve the original error when wrapping. A stack trace that stops at your
  wrapper is a debugging session someone else will pay for.

## Before you say it is done

Run through this honestly:

- [ ] The whole suite passes, and no test was weakened to make it pass
- [ ] Lint and type checks clean, with no new suppressions or `any`
- [ ] The diff contains nothing that was not asked for
- [ ] No debug output, no `TODO` without an issue number, no commented-out code
- [ ] No secrets, keys, tokens or real customer data anywhere in the diff
- [ ] You have read your own diff top to bottom

Then go to [`ship-pr`](../ship-pr/SKILL.md).

## Failure modes

- **The drifting diff.** You went in to fix a bug and came out with a refactor.
  Stash the refactor, land the fix, open an issue.
- **Weakening a test to make it pass.** If a test now fails, either your change is
  wrong or the test encoded a behaviour you deliberately changed. Decide which, and
  say so in the commit. Never loosen an assertion to get green.
- **Claiming done without running anything.** Run the commands. Paste the output.
- **Mock-shaped success.** Tests that pass because everything real was mocked out
  prove only that the mocks agree with each other.
- **Silent scope refusal.** If a step turns out to be wrong, stop and say so.
  Delivering something adjacent to what was asked, without flagging it, wastes the
  reviewer's time and your own.

## When to stop and escalate

Immediately, per [house rules](../../../docs/house-rules.md), if the change requires
deleting data, an irreversible migration, or touches auth, crypto or payments —
or if the plan turns out to be based on a wrong assumption. Report what you found
and what you would do instead. Do not improvise past it.
