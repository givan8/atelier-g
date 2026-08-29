# Python conventions

The principles live in [atelier-g](https://github.com/givan8/atelier-g) —
`skills/write-tests`, `skills/implement-change`, `docs/house-rules.md`. This file
is only the mechanics that differ by language.

## Layout

```
src/app/                   application code, src layout so tests import it as installed
src/app/<feature>.py       group by feature, not by technical layer
tests/test_<feature>.py    mirrors src/app
```

No `utils.py`. A module named after what it contains is findable; a module named
after nothing accumulates everything.

## Tests

- Runner: pytest. Plain functions and `assert` — no unittest classes.
- Name the test after the behaviour:
  `def test_rejects_a_signup_when_the_email_is_already_registered() -> None:`
- Fixtures only for genuine setup and teardown. A fixture that just builds a value
  is better as a factory function with defaults.
- `pytest.raises` always with `match=` — otherwise the test passes on the wrong
  exception.
- Never `time.sleep`. Inject the clock, as `health()` does.

## Types

- `mypy --strict`, and no loosening it per module.
- Annotate every public function, parameter and return, including `-> None`.
- No bare `Any`. Narrow `object` or use a protocol.
- `from __future__ import annotations` at the top of every module.
- Frozen dataclasses with `slots=True` for data. Mutable default arguments never.

## Errors

- Define one exception type per failure domain, subclassing a project base.
- Messages name the thing that failed and the value that caused it.
- Never a bare `except:` and never `except Exception: pass`. If an error is
  genuinely expected and safe, the handler carries a comment saying why.
- `raise ... from err` when wrapping, so the original traceback survives.

## Style

- Ruff for lint and import order; it is the arbiter, not personal preference.
- Line length 100.
- f-strings for formatting; `!r` when quoting a value in an error message.
- Standard library first. A dependency is a standing cost and needs a reason in
  the PR body.
