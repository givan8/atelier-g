# AGENTS.md

Harness-neutral entry point for atelier-g.

This file exists because different agent harnesses look for different filenames.
The content is identical to [`CLAUDE.md`](CLAUDE.md) — read either one.

If you are an agent that found this file first: read `CLAUDE.md`, then
`docs/house-rules.md`, then the skill in `skills/` that matches your task.
Nothing in this repository requires a specific harness, model or tool. Skills are
plain Markdown with YAML frontmatter (`name`, `description`, optional
`when_to_use`) and can be loaded, inlined, or simply read as documentation.

The canonical skill library is `skills/`. Any directory named after a specific
harness (`.claude/`, and any others added later) is generated output and will be
overwritten by `./scripts/sync-harnesses.sh`.
