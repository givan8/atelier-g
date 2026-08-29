# TypeScript conventions

The principles live in [atelier-g](https://github.com/givan8/atelier-g) —
`skills/write-tests`, `skills/implement-change`, `docs/house-rules.md`. This file
is only the mechanics that differ by language.

## Layout

```
src/                       application code, flat until it hurts
src/<feature>/             group by feature, not by technical layer
src/<name>.test.ts         tests live beside the code they test
```

No `utils.ts`. A file named after what it contains is findable; a file named
after nothing accumulates everything.

## Tests

- Runner: `node:test` from the standard library. No test framework dependency
  until something genuinely needs one.
- Name the test after the behaviour, as a sentence:
  `test("rejects a signup when the email is already registered")`.
- `node --test` picks up `*.test.ts`. Keep them beside the source.
- Assert with `node:assert/strict`. Never the loose variants.

## Types

- `strict: true`, and no loosening it per file.
- No `any`. If you truly need an escape hatch use `unknown` and narrow it.
- No `@ts-expect-error` without a comment saying why and what would remove it.
- Prefer `type` aliases for data shapes and `interface` for things that are
  implemented. Do not mix both for the same concept.
- Parse at the boundary: validate external input into a typed shape once, and
  trust the type inside.

## Errors

- Throw `Error` subclasses with a message that names the thing that failed and
  the value that caused it.
- Never `catch (e) {}`. If an error is genuinely expected and safe, the catch
  carries a comment saying why.
- Preserve the original: `throw new ConfigError("...", { cause: err })`.

## Async

- `async`/`await` only — no raw `.then()` chains.
- Every promise is awaited or explicitly handled. A floating promise is a lost
  error.
- No `sleep` in tests. Inject the clock, as `health()` does.

## Modules

- ESM only (`"type": "module"`). Explicit `.ts` extensions on relative imports.
- No default exports. Named exports are greppable and rename safely.
- Dependencies are a standing cost: each one needs a reason in the PR body.
