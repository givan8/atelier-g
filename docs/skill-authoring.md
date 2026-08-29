# Writing a skill

A skill is a procedure that raises the floor on a recurring task. It is written for
whoever does the task next — a model, or a person on their first week.

## When a skill is warranted

Write one when **all** of these hold:

- The task recurs. Once is a note in a PR; three times is a skill.
- Doing it badly is common and costly, and doing it well is teachable.
- The right procedure is stable — it will not be obsolete next quarter.

Do **not** write a skill for a one-off, for something a linter can enforce, or for
knowledge the model already has. "How to write a for loop" is not a skill. "What a
reviewable diff looks like here" is.

## Structure

```
skills/<kebab-case-name>/
├── SKILL.md            required
├── checklist.md        optional — long lists the skill links to
└── examples/           optional — reference files, before/after pairs
```

`SKILL.md` frontmatter:

```yaml
---
name: review-code
description: >
  Use when reviewing a diff, pull request, or patch — yours or someone else's.
  Covers what to look for, in what order, and how to phrase findings.
---
```

`name` must equal the directory name. `description` is the **trigger**: write it as
the conditions under which the skill applies, in the words someone would use to
describe their situation. A harness matches against this text to decide whether to
load the skill, so "Use when reviewing a diff…" beats "A guide to code review".

## Body

Aim for under 150 lines. Structure that works:

1. **One line on what good looks like.** The outcome, not the process.
2. **The procedure**, as ordered steps. Imperative voice. Each step should be
   something you can tell whether you did.
3. **Failure modes** — what people get wrong here, stated as "if X, do Y".
4. **When this skill does not apply**, and what to do instead.

Rules for the prose:

- Address the reader as "you". Never "the agent should".
- Be concrete. Name commands, filenames, error strings.
- Every rule needs an escape hatch: state what to do when it cannot be followed.
- No preamble. The first sentence carries information.
- If a section only restates the house rules, delete it and link instead.

## What to keep out

- **Harness syntax.** No tool names, no slash commands, no XML tags a specific
  product understands. A skill must read correctly to a human. See ADR-0002.
- **Model-specific prompting.** "Think step by step" is not a house standard.
- **Duplicated policy.** House rules live in `docs/house-rules.md`. Link to them.
- **Anything that goes stale.** Version numbers, headcounts, current project names.

## Testing a skill

Every behavioural change needs an eval case in `evals/cases/`:

```yaml
# evals/cases/review-code-flags-swallowed-error.yaml
skill: review-code
prompt: |
  Review this diff:
  ...
  + try { save(x) } catch (e) {}
expect_contains: ["swallow", "error"]
expect_absent: ["looks good to me"]
```

Then:

```bash
./scripts/validate-skills.py    # structure
./evals/run.py --skill review-code
```

A case should fail against the old version of the skill. If it passes either way,
it is not testing your change.

## Changing an existing skill

- Edit `skills/<name>/SKILL.md`. Never `.claude/`.
- Run `./scripts/sync-harnesses.sh` and commit the regenerated output.
- Explain in the PR body what was going wrong that made the change necessary. A
  skill diff without a reason is unreviewable.
- Deleting a skill is fine and often correct. Skills that no longer match how the
  shop works are worse than no skill, because they are followed anyway.
