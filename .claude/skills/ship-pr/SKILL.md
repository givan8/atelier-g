---
name: ship-pr
description: >
  Use when turning finished work into a pull request — writing the description,
  checking the diff is reviewable, and knowing when it is genuinely ready. Use
  after implement-change and before asking anyone to look.
---

<!-- GENERATED FROM skills/ship-pr/SKILL.md — DO NOT EDIT. Run ./scripts/sync-harnesses.sh -->

# Ship a pull request

The PR is where your work meets other people. Its job is to make review cheap: the
reviewer should understand why this exists before they read a line of the diff.

## Before opening

- Rebase on the current default branch and re-run the full suite. Green on a stale
  base means nothing.
- Read your own diff top to bottom in the PR view. See
  [`review-code`](../review-code/SKILL.md) — do the passes on your own work.
- Check the diff for anything unintended: stray files, formatting churn from an
  editor, a debug line, a lock file you did not mean to update.
- Confirm the [definition of done](../../../docs/house-rules.md#definition-of-done).

## Size

If the diff is over roughly 400 lines of real change, split it. Reviews degrade
sharply past that point, and a large PR gets a worse review exactly when it needs a
better one.

Ways to split: mechanical refactor first and behaviour change second; new code
unused, then wired up; one commit per plan step, each landing separately.

If it genuinely cannot be split — a generated file, a rename across the tree — say
so at the top of the description and tell the reviewer which files matter.

## Description

```markdown
## Why
The problem, in the reader's terms. Link the issue. If this is not obvious from
the title, this section is the most important part of the PR.

## What changed
Two to five bullets. The shape of the change, not a file listing.

## How it was verified
The commands you ran and what happened. For a bug fix: evidence the test failed
before and passes now.

## Risk and rollback
What could go wrong, what to watch after deploy, how to revert. Say "low risk,
plain revert" when that is true.

## Notes for the reviewer
Where to start, what you are unsure about, what you deliberately left out.
```

Write it for someone who was not in the conversation, because in six months that
will include you.

## Commits

- Imperative mood, one logical change each: `fix: reject empty tenant id`.
- Squash the noise — `wip`, `fix lint`, `oops` — before requesting review.
- Keep genuine steps as separate commits; a reviewer can then read them in order.
- If the repository uses conventional commit types, follow it exactly; releases
  and changelogs may be generated from it.

## Asking for review

Say what kind of review you want: a correctness check, a design opinion, a quick
look at one file. An unqualified "PTAL" gets an unqualified review.

Flag your own uncertainty. "I am not sure the retry logic is right" gets that part
read properly, and costs you nothing.

## Responding to review

- Answer every comment, even if only to say you disagree and why.
- Push fixes as new commits during review so the reviewer can see what changed;
  squash at merge if the repository does that.
- When you disagree, say so with a reason. Silent compliance produces code nobody
  believes in; silent refusal produces a second round of the same comment.
- Do not merge over an unresolved blocking finding, including your own.

## Before merge

- [ ] All blocking findings resolved
- [ ] CI green on the current head, not an earlier commit
- [ ] Description still describes the change after review edits
- [ ] Any decision that emerged in discussion is captured in an
      [ADR](../write-adr/SKILL.md) or an issue — not left in comment threads
- [ ] Follow-ups you promised exist as issues

## Failure modes

- **The description that restates the diff.** "Added a function to X." The
  reviewer can see that. Tell them why.
- **The PR nobody can review.** Twelve hundred lines, four unrelated concerns.
- **Green CI on a stale base.** Rebase and re-run.
- **Merging your own unreviewed work** because it is small and you are confident.
  The small confident ones are the ones that page you.
- **Losing the discussion.** A decision argued out in comments and never written
  down is a decision that will be re-argued.
