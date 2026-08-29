# atelier-g

The operating system for a software factory run by AI agents.

This repository is not an application. It is the **encoded way the company works** —
the roles, gates, conventions and skills that any capable agent reads before it
touches code. Point an agent at a request and at this repo, and the work should
come out looking like it came from the same shop as everything else.

An atelier is a small studio where work is made to a house standard. The standard
lives here.

---

## The idea in one paragraph

Most "AI coding" setups put the intelligence in the prompt and lose it when the
session ends. This repo inverts that: the durable part — how we establish what is
being asked for, how we specify it, who checks it, what a reviewable change looks
like — lives in version control as plain Markdown, and the model is the
interchangeable part. A new model, a new harness, or a new engineer all get
productive by reading the same files.

## Every request goes through one door

[`skills/route-request`](skills/route-request/SKILL.md) decides which of four
paths a request takes, and says which it chose:

| Path | When | What happens |
|---|---|---|
| **Answer** | The request asks for information | Just answer it. No issue, no pipeline. |
| **Fast path** | A change meeting all six trivial criteria | Straight to implement and ship |
| **Enhancement** | Changing something that exists | [Enhancement delivery](workflows/enhancement-delivery.md) — analyst first |
| **New project** | Nothing exists yet | [New project delivery](workflows/new-project-delivery.md) — engagement first |

The six trivial criteria are written down, and the router may not stretch them.
That is deliberate: a fast path governed by judgement in the moment always widens
until the pipeline is decorative.

## The delivery pipeline

```
 new project    engagement-manager ──▶ brief ──▶ [user confirms]
                                                       │
 both           business-analyst ──▶ specification ──▶ [user confirms]
                                          │
                                     issue set
                                          │
                tech-lead ──▶ sequenced and assigned
                                          │
                   ┌──────────────────────┴──────────────────────┐
                   ▼                                             ▼
          principal-engineer                             infra-engineer
                   └──────────────────────┬──────────────────────┘
                                          ▼
                              tech-lead reviews every change
                                          │
                                    qa-engineer ──▶ report
                                          │
                              business-analyst verifies
                                          │
                       ┌──────────────────┴──────────────────┐
                  criteria unmet                        all criteria met
                       │                                     │
                  reopen issues,                        [user signs off]
                  back to tech-lead                     close issues
```

Three rules make it mean something: no role grades its own work; a handoff is an
artefact, not a conversation; and the two confirmation gates belong to the user.
See [ADR-0004](docs/adr/0004-role-based-delivery-pipeline.md).

## Layout

```
skills/          What good work looks like. Harness-neutral Markdown. Source of truth.
roles/           Who owns each stage, what they may decide, what they may not do.
workflows/       The order of stages, and the artefact that gates each one.
docs/            House rules, architecture, authoring guides, ADRs.
templates/       Starting points for new projects (polyglot).
evals/           Cases that check skills and roles still behave.
scripts/         Sync, validation and scaffolding tooling.
.claude/         Generated projection — skills, commands and subagents. Do not hand-edit.
CLAUDE.md        Entry point for Claude Code.
AGENTS.md        Entry point for every other harness.
```

Read [`docs/architecture.md`](docs/architecture.md) for why it is split this way.

## Quick start

```bash
git clone https://github.com/givan8/atelier-g
cd atelier-g
./scripts/sync-harnesses.sh     # project skills/ and roles/ into .claude/
./scripts/validate.py           # frontmatter, naming, structure, links
```

Then, to start a project under the house standard:

```bash
./scripts/new-project.sh my-service --template service-ts
```

## The skills

| Skill | Use it when |
|---|---|
| [`route-request`](skills/route-request/SKILL.md) | **Any request arrives** |
| [`manage-issues`](skills/manage-issues/SKILL.md) | Writing, picking up or closing an issue |
| [`plan-feature`](skills/plan-feature/SKILL.md) | A request needs scoping before code |
| [`implement-change`](skills/implement-change/SKILL.md) | Executing an agreed plan |
| [`write-tests`](skills/write-tests/SKILL.md) | Adding or repairing coverage |
| [`review-code`](skills/review-code/SKILL.md) | Reviewing a diff |
| [`ship-pr`](skills/ship-pr/SKILL.md) | Turning finished work into a PR |
| [`triage-issue`](skills/triage-issue/SKILL.md) | An inbound issue needs a decision |
| [`scaffold-project`](skills/scaffold-project/SKILL.md) | Starting a new service or package |
| [`write-adr`](skills/write-adr/SKILL.md) | A decision will outlive the conversation |

## Using it elsewhere

**Claude Code** — clone and run the sync script, or add it as a submodule. Skills
land in `.claude/skills/`, roles become subagents in `.claude/agents/`, and slash
commands in `.claude/commands/`.

**Any other harness** — read `AGENTS.md` and the `skills/` and `roles/`
directories directly. Everything is plain Markdown with YAML frontmatter and no
harness-specific syntax; that constraint is deliberate, see
[ADR-0002](docs/adr/0002-harness-neutral-skills.md). Without subagents, one agent
adopts each role in turn and re-reads the charter at every handoff.

**A human** — the skills and charters read as onboarding docs, because that is
what they are.

## Contributing

Skills, roles and workflows change through PRs like anything else. A change needs
a reason in the PR body and, if it changes behaviour, an eval case that would have
failed before. See [`docs/skill-authoring.md`](docs/skill-authoring.md).

## Licence

MIT. See [LICENSE](LICENSE).
