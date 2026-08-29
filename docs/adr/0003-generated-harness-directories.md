# 3. Harness directories are generated, not authored

- **Status:** Accepted
- **Date:** 2026-08-29

## Context

[ADR-0002](0002-harness-neutral-skills.md) puts the canonical library in `skills/`.
But Claude Code looks in `.claude/skills/`, and other harnesses will look
elsewhere. Something has to bridge the two.

Three options exist: symlink, copy at install time, or generate and commit. The
choice matters more than it looks, because the failure mode of getting it wrong is
silent — someone edits the copy, their improvement works locally, and it is
destroyed by the next sync.

## Decision

`scripts/sync-harnesses.sh` generates `.claude/` from `skills/`, and the generated
output **is committed**. Every generated file carries a header:

```
<!-- GENERATED FROM skills/<name>/SKILL.md — DO NOT EDIT. Run ./scripts/sync-harnesses.sh -->
```

CI (`.github/workflows/skills.yml`) re-runs the sync and fails if the working tree
changes, which catches both a hand-edit and a forgotten sync in the same check.

## Consequences

**Good.** Cloning the repo gives a working Claude Code setup with no build step —
which matters, because the first thing anyone does is clone and try it. The
generated files are visible in review, so a bad sync is caught by a human reading
the diff. Symlinks, which break on Windows and confuse some tooling, are avoided.

**Bad.** Every skill change produces a two-file diff, and the second file is noise.
Reviewers must learn to skim generated output. There is a real chance someone edits
the generated copy anyway; the header and the CI check are the defence, and neither
is perfect.

**Accepted cost.** Duplication in the repository in exchange for zero setup
friction and reviewable output.

## Alternatives considered

**Symlink `.claude/skills` → `../skills`.** Tempting and nearly free. Rejected:
symlinks in git are fragile across platforms, and the harness-specific pieces —
commands, settings — cannot be symlinked anyway, so we would need the sync script
regardless and would then have two mechanisms.

**Generate at install time, gitignore the output.** Rejected: a fresh clone would
not work until someone ran a script they did not know about, and the generated
output would never be reviewed.

**Put the canonical library directly in `.claude/` and generate the others from
it.** Rejected: it privileges one harness in the layout and quietly invites
product-specific syntax back into the source of truth, undoing ADR-0002.
