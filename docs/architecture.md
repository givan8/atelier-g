# Architecture of this repository

## The problem it solves

An agent is only as good as the context it is given, and context assembled by hand
in a chat window dies with the session. The useful, durable part of "how we build
software" — the standards, the checklists, the shape of a good PR — is stable for
years. The model that reads it changes every few months.

So: put the stable part in git, keep it in a format any model can read, and make
the volatile part (which harness, which model, which session) swappable.

## Source of truth and projections

```
                 skills/            ← canonical, harness-neutral, hand-edited
                    │
    ./scripts/sync-harnesses.sh
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
  .claude/skills/         (future harness dirs)
  .claude/commands/        generated, never hand-edited
```

One directory is written by humans and agents. Everything harness-shaped is
generated from it. This means:

- A skill improvement lands once and reaches every harness.
- A new harness costs one function in the sync script, not a fork of the library.
- Diffs stay readable, because generated files are regenerated rather than patched.

The sync script writes a header into every generated file marking it as generated.
CI fails if a generated file has been edited by hand (`.github/workflows/skills.yml`).

## Why Markdown and not code

A skill is a procedure a competent person could follow. Encoding it as code would
mean choosing a runtime, a schema and a version, and it would stop being readable
by a new engineer on day one. Markdown with light frontmatter keeps the library
legible to humans, greppable, diffable, and loadable by any harness that wants to
parse it.

The trade-off is that nothing enforces a skill's content. That is what
`scripts/validate-skills.py` and `evals/` are for: structure is validated
mechanically, behaviour is validated by cases.

## Directory responsibilities

**`skills/<name>/SKILL.md`** — one procedure, self-contained, under ~150 lines.
Frontmatter declares `name` and `description`; the description is what a harness
matches against when deciding whether the skill applies, so it is written as
triggering conditions, not as a summary. Supporting material (checklists, long
references, example files) goes in the skill's own directory and is linked from
`SKILL.md`, so it is loaded only when needed.

**`workflows/`** — sequences that compose skills into an end-to-end unit of work.
A skill answers "how do I do X well"; a workflow answers "what is the order of
operations from issue to merged PR". Workflows are prose, not scripts, so a human
can run them too.

**`docs/`** — the standards themselves (`house-rules.md`), how to extend the
library (`skill-authoring.md`), this file, and `adr/` for decisions with dates and
consequences.

**`templates/`** — starting points for new projects. `_shared/` holds files common
to every language (editorconfig, PR template, the agent entry point that points
back here); language directories layer their own tooling on top. Templates carry
the house standard into new repos; without them, every new project drifts.

**`evals/`** — cases that check a skill still does its job. Each case is a task
description plus assertions about what a correct response contains or avoids. The
runner is deliberately simple and harness-agnostic: it emits the prompts and checks
recorded outputs, so it can be driven by CI, by a local model, or by a human
reading the results.

**`scripts/`** — the small amount of automation this repo owns. No dependencies
beyond Python 3 standard library and POSIX shell, so it runs anywhere without a
setup step.

## Polyglot stance

Skills are written to be language-agnostic; where a rule genuinely differs by
language, the skill states the principle and defers specifics to the template. For
example, `write-tests` says "one assertion per behaviour, name the test after the
behaviour" — true in any language — and leaves the test runner, layout and naming
convention to `templates/service-ts` or `templates/service-py`.

The rule for adding a language: it needs a template and a conventions file, not new
skills. If you find yourself writing `implement-change-rust`, the original skill
was too specific.

## What this repository deliberately does not do

- **It does not run agents.** No orchestration layer, no queue, no daemon. CI can
  invoke an agent, but the repo's job is to define standards, not to execute them.
- **It does not vendor a model.** Nothing here names a model version or depends on
  one's quirks.
- **It does not hold application code.** Projects generated from `templates/` live
  in their own repositories and reference this one.
