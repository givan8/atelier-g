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

```toml
# evals/cases/review-code-flags-swallowed-error.toml
skill = "review-code"
rationale = "Reviews kept approving empty catch blocks; house rule 6 says fail loudly."

prompt = """
Review this diff:
...
+ try { save(x) } catch (e) {}
"""

expect_contains = ["swallow", "error"]
expect_absent = ["looks good to me"]
```

Then:

```bash
./scripts/validate.py    # structure
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

---

# Writing a role charter

A role says *who owns a stage, what they may decide, and what they hand on*. Write
one only when a stage needs an owner distinct from the stages either side of it —
if the same party can reasonably do both, it is one role.

## Structure

```
roles/<kebab-case-name>/ROLE.md
```

Frontmatter: `name` (matching the directory), `description` (when to **dispatch**
this role — a harness matches on this text), and `access`:

- `read-only` — may read, search and run commands, but cannot edit files
- `read-write` — may edit files and run commands

Name no tools. The sync script translates `access` into whatever each harness
calls permissions, per [ADR-0002](adr/0002-harness-neutral-skills.md).

## Body, in this order

1. **What you own** — one or two sentences, and why the role is separate.
2. **What you are given** — the artefact from the previous stage.
3. **What you produce** — the artefact, with its shape shown.
4. **Method** — how to do it well, as ordered steps.
5. **Gate** — what must be true before the next stage starts. Falsifiable.
6. **You may decide alone** — so the role does not escalate everything.
7. **You must escalate** — and to whom: another role, or the user.
8. **You may not** — required. `validate.py` fails a charter without it.

## Why "You may not" is mandatory

A role without boundaries collapses into doing the whole thing, and then the same
party specifies, builds and verifies. That is not verification — it is one party
agreeing with itself three times, which is the failure the role layer exists to
prevent.

Write the boundaries as the specific temptations of that role, not as generic
caution. "Do not fix what you find" for QA. "Do not write the implementation and
then review it" for the tech lead. "Do not change acceptance criteria to match
what was built" for the analyst. Each of those is a thing that role will actually
be tempted to do at 5pm on a Friday.

## Testing a charter

Same as a skill: an eval case in `evals/cases/` that would have failed before your
change. Charter cases usually assert a refusal — that the role escalated rather
than deciding, or declined work belonging to another role.
