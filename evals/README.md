# Evals

Structure is checked by `scripts/validate-skills.py`. Behaviour is checked here.

A case is a task plus assertions about what a correct response contains or avoids.
The runner does not call a model: it emits prompts, and scores recorded responses.
That keeps the cases usable from any harness, from CI, or by a person writing the
response by hand — and it keeps this repository dependency-free.

## Running

```bash
./evals/run.py                      # score every case that has a recording
./evals/run.py --skill review-code  # one skill
./evals/run.py --emit ./prompts     # write prompt files to run somewhere
./evals/run.py --strict             # missing recordings are failures (CI)
```

The loop:

1. `./evals/run.py --emit ./prompts` writes one prompt per case.
2. Run each prompt in your harness of choice, with the repository available.
3. Save each response to `evals/outputs/<case-id>.txt`.
4. `./evals/run.py` scores them.

`evals/outputs/` is gitignored. Recordings are evidence for one run, not artefacts
to maintain.

## Writing a case

```toml
# evals/cases/review-code-flags-swallowed-error.toml
skill = "review-code"
rationale = "Reviews kept approving empty catch blocks; house rule 6 says fail loudly."

prompt = """
Review this diff:

  def save_profile(user):
+     try:
+         db.write(user)
+     except Exception:
+         pass
      return user
"""

expect_contains = ["error", "swallow"]
expect_absent   = ["looks good to me"]
expect_matches  = ["blocking|should fix"]
```

- `expect_contains` / `expect_absent` — case-insensitive substrings
- `expect_matches` — regular expressions, case-insensitive, multiline
- `rationale` — why the case exists. Printed on failure, so the next person knows
  what was going wrong that made this worth pinning down.

A case with no assertions is rejected by the runner: it cannot fail, so it is not
a test.

## What makes a good case

- **It would have failed before your change.** If it passes against the old skill,
  it is not testing anything.
- **It asserts a decision, not a phrasing.** Assert that a swallowed error is
  flagged, not that the response uses a particular sentence.
- **It is small.** One behaviour per case, same as any test.
- **It captures a real failure.** The best cases come from something an agent
  actually got wrong. Write the case at that moment.

Assertions on natural language are inherently loose. Prefer several tolerant
assertions over one exact-match string — a case that fails on a synonym trains
people to ignore the suite.
