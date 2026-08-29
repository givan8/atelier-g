# Workflow: new project

From "we should build a thing" to a repository that is safe to put work into.

---

## 1. Justify → a written reason

**Skill:** `scaffold-project` (step 1)
**Artefact:** one paragraph on why this cannot live inside an existing repository.

A new repository is a permanent obligation — CI, dependencies, secrets, access,
releases, a README to keep true. Different deployment lifecycle, security boundary
or owning team justify it. A different language or a feeling of tidiness do not.

**Gate:** if the paragraph is hard to write, it is not a new repository.

## 2. Generate → a repository from a template

**Skill:** `scaffold-project`
**Artefact:** `./scripts/new-project.sh <name> --template <template>` has run, and
the output is committed as one commit.

No hand-rolling. If no template fits, use the nearest one and open an issue against
atelier-g for the gap — a template that never gets fixed is how conventions
diverge.

## 3. Prove → a green first build

**Artefact:** CI green on the first commit, and a clean-clone install that follows
the README exactly and works.

Check, by actually running them:

- [ ] Install from clean clone per the README
- [ ] Tests run and pass
- [ ] Lint and type check pass
- [ ] Service starts and answers a health check
- [ ] CI green

**Gate:** a scaffold whose CI has never been green is not a scaffold. Do not build
features on top of it.

## 4. Record → the first ADR

**Skill:** `write-adr`
**Artefact:** `docs/adr/0001-*.md` — why this project exists, the shape chosen, the
alternatives rejected.

This is the single most useful ADR the project will ever have and the one most
often skipped, because at this moment the reasoning feels too obvious to write
down. It will not be obvious in a year.

## 5. Own → a name on it

**Artefact:** `CODEOWNERS` naming who is responsible when it breaks, and an entry
in whatever inventory of services you keep.

**Gate:** an unowned repository is an outage with no assignee.

## 6. Hand over → an entry point that works

**Artefact:** `AGENTS.md` and `CLAUDE.md` in the new repository pointing back at
atelier-g, and a README that describes what the project does rather than what it
will do.

Verify by asking an agent, in a fresh session with no context, to make a trivial
change. If it cannot orient itself from the repository alone, the entry point is
wrong — fix it now, while the fix is cheap.

---

## Then

The first real change follows [`issue-to-merge.md`](issue-to-merge.md) like any
other. Resist adding structure the project does not yet need: no abstraction with
one implementation, no second environment before the first works, no service split
before the monolith hurts.
