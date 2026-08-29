# Templates

Starting points for new projects. Templates are how the house standard reaches new
repositories; without them, every project drifts within a month.

| Template | For |
|---|---|
| `service-ts` | A TypeScript/Node service. `node:test`, strict `tsc`, no framework. |
| `service-py` | A Python service. pytest, ruff, `mypy --strict`, stdlib only. |
| `_shared` | Files every project gets, whatever the language. Copied over the template. |

## Use

```bash
../scripts/new-project.sh billing-webhooks --template service-ts
```

Then follow [`../workflows/new-project.md`](../workflows/new-project.md). A
scaffold whose CI has never been green is not a scaffold.

## What `_shared` contains

`AGENTS.md` and `CLAUDE.md` pointing back at atelier-g, the ADR template, the PR
template, `CODEOWNERS`, `.editorconfig`, `.env.example`. It is copied *after* the
language template, so it wins on conflict.

## Placeholders

`{{PROJECT_NAME}}`, `{{TEMPLATE}}` and `{{YEAR}}` are substituted by
`new-project.sh` across Markdown, JSON, TOML and YAML files.

## Adding a language

A new language needs a template directory and a `CONVENTIONS.md` — **not new
skills**. The skills are language-agnostic on purpose; if you find yourself
writing `implement-change-rust`, the original skill was too specific and should be
generalised instead.

A template must, on day one: install from a clean clone by following its own
README, run its tests with one command, pass lint and type checks, start and answer
a health check, and go green in CI. If it does not do all five, it is not ready to
be a template.

## Keeping them honest

When you fix something in a generated project that was wrong in the template, fix
the template in the same PR. Template drift is how a standard quietly stops being
one.
