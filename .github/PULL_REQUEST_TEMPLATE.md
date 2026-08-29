## Why

<!-- What was going wrong that made this change necessary? A skill diff without a
     reason is unreviewable. -->

## What changed

-

## Evidence

<!-- For a skill change: the eval case that would have failed before, and its
     result now. For tooling: the command output. -->

```
```

---

- [ ] `./scripts/validate.py` passes
- [ ] `./scripts/sync-harnesses.sh` has been run and `.claude/` is committed
- [ ] Behavioural changes have an eval case in `evals/cases/`
- [ ] No harness-specific syntax in `skills/` or `roles/` (ADR-0002)
- [ ] Decisions worth keeping are in `docs/adr/`
