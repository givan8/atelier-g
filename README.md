# atelier-g

The operating system for a software factory run by AI agents.

This repository is not an application. It is the **encoded way the company works** —
the conventions, skills, workflows, templates and checks that any capable agent
reads before it touches code. Point an agent at a task and at this repo, and it
should produce work that looks like it came from the same shop as everything else.

An atelier is a small studio where work is made to a house standard. The standard
lives here.

---

## The idea in one paragraph

Most "AI coding" setups put the intelligence in the prompt and lose it when the
session ends. This repo inverts that: the durable part — how we plan, how we test,
what a reviewable change looks like, when we write things down — lives in version
control as plain Markdown, and the model is the interchangeable part. A new model,
a new harness, or a new engineer all get productive by reading the same files.

## Layout

```
skills/          Canonical skill library. Harness-neutral Markdown. Source of truth.
workflows/       Multi-skill procedures — how a unit of work moves end to end.
docs/            House rules, architecture, skill authoring guide, ADRs.
templates/       Starting points for new projects (polyglot).
evals/           Test cases that check skills still trigger and still work.
scripts/         Sync, validation and scaffolding tooling.
.claude/         Claude Code projection — generated from skills/. Do not hand-edit.
.github/         CI: skill validation, evals, agent-assisted review.
CLAUDE.md        Entry point for Claude Code.
AGENTS.md        Entry point for every other harness. Same content, different name.
```

Read [`docs/architecture.md`](docs/architecture.md) for why it is split this way.

## Quick start

```bash
git clone https://github.com/givan8/atelier-g
cd atelier-g
./scripts/sync-harnesses.sh     # project skills/ into .claude/ and friends
./scripts/validate-skills.py    # check frontmatter, naming, structure
```

Then, from any repo where you want the house standard to apply:

```bash
./scripts/new-project.sh my-service --template service-ts
```

## Using the skills

**Claude Code** — clone this repo and run the sync script, or add it as a submodule
under `.claude/`. Skills land in `.claude/skills/` and slash commands in
`.claude/commands/`.

**Any other harness** — read `AGENTS.md` and the `skills/` directory directly. Every
skill is a self-contained Markdown file with YAML frontmatter and no
harness-specific syntax. That constraint is deliberate; see
[ADR-0002](docs/adr/0002-harness-neutral-skills.md).

**A human** — the skills read as onboarding docs, because that is what they are.

## The skills

| Skill | Use it when |
|---|---|
| [`plan-feature`](skills/plan-feature/SKILL.md) | A request needs scoping before any code is written |
| [`implement-change`](skills/implement-change/SKILL.md) | Executing an agreed plan against the codebase |
| [`write-tests`](skills/write-tests/SKILL.md) | Adding or repairing test coverage |
| [`review-code`](skills/review-code/SKILL.md) | Reviewing a diff, yours or someone else's |
| [`ship-pr`](skills/ship-pr/SKILL.md) | Turning finished work into a mergeable PR |
| [`triage-issue`](skills/triage-issue/SKILL.md) | An inbound issue or request needs a decision |
| [`scaffold-project`](skills/scaffold-project/SKILL.md) | Starting a new service or package |
| [`write-adr`](skills/write-adr/SKILL.md) | A decision will outlive the person who made it |

## Contributing

Skills change through PRs like anything else. A skill change needs a reason in the
PR body and, if it changes behaviour, an eval case that would have failed before.
See [`docs/skill-authoring.md`](docs/skill-authoring.md).

## Licence

MIT. See [LICENSE](LICENSE).
