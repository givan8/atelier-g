# House rules

The non-negotiables. Everything in `skills/` is an elaboration of something here.
If a skill and this document disagree, this document wins and the skill is a bug.

---

## 1. Understand before you change

No edit lands without first reading the code around it. "It compiled" is not
understanding. If you cannot state what the existing code does and why, you are
not ready to change it.

Corollary: when a request is ambiguous, the cost of asking one question is always
lower than the cost of building the wrong thing. Ask. Then build.

## 2. Small, reversible, explained

A change should be small enough to review in one sitting, reversible by a single
revert, and accompanied by a sentence explaining why it exists. Big changes are
sequences of small ones, not exceptions to the rule.

## 3. Tests are the specification

If behaviour matters, a test asserts it. New behaviour arrives with a test; fixed
bugs arrive with a test that fails on the old code. Coverage percentage is not a
goal — a test that would catch the regression is.

## 4. Make the state legible

Anyone — human or agent — landing on this codebase cold should be able to work out
what is going on from the repository alone. That means: honest READMEs, ADRs for
decisions, comments that explain *why* rather than *what*, and no tribal knowledge
that lives only in someone's head or in a chat log.

## 5. Boring by default

Choose the well-understood option unless there is a written reason not to. Novelty
is a cost paid by everyone who touches the code afterwards. When you do choose the
interesting option, that is an ADR.

## 6. Fail loudly

No silent catches, no swallowed errors, no defaults that paper over a missing
value. If something is wrong, the system says so at the earliest point it can, with
enough context to act on.

## 7. Secrets never enter the repository

Not in code, not in tests, not in fixtures, not in a commit that gets amended
later. Configuration comes from the environment. If you think you need a secret in
the repo, you need a different design.

## 8. Agents follow the same rules as humans

An agent's PR is held to the standard of a human's PR — same review, same tests,
same commit hygiene. Nothing merges because a model wrote it. Correspondingly,
agents get the same courtesies: clear task definitions, access to context, and the
right to say a request is underspecified.

## 9. Leave the campsite cleaner

Fix the small adjacent thing — the typo, the misleading name, the dead import —
when you are already in the file. Do not turn it into a refactor. If the cleanup is
bigger than the change that revealed it, open an issue instead.

## 10. Write it down at the moment of decision

The reasoning is available for about an hour after a decision is made and then it
is gone forever. ADRs, PR bodies and commit messages are all cheap at the moment of
decision and impossible to reconstruct later.

---

## Definition of done

A unit of work is done when *all* of these are true:

- [ ] The change does what was asked, and nothing that was not asked
- [ ] Tests exist for the new behaviour, and the whole suite passes
- [ ] Linting and type checks pass with no new suppressions
- [ ] The PR body explains why, not just what
- [ ] Any decision worth remembering is captured in an ADR
- [ ] Documentation that is now wrong has been corrected
- [ ] No secrets, no debug output, no commented-out code left behind

## Escalate rather than guess

Stop and ask a human when you hit any of these:

- The task requires deleting data, dropping a table, or a non-reversible migration
- Authentication, authorisation, cryptography or payment handling is involved
- The change touches something the tests do not cover and you cannot cover it
- Two house rules conflict for this specific case
- Requirements contradict each other and both have a plausible reading

Escalating is not failure. Guessing quietly is.
