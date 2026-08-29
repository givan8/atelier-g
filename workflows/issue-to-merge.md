# Workflow: issue to merge

The default path for a unit of work. Prose, not a script — a human can run it too.

Each stage names the skill that governs it and the artefact that must exist before
the next stage starts. **If the artefact does not exist, the stage is not done**,
regardless of how much work happened.

---

## 1. Triage → a decision

**Skill:** `triage-issue`
**Artefact:** a comment on the issue stating the classification and the decision,
with a reason.

Ends here for most issues: duplicate, won't do, question answered, needs
information. Only "fix now", "accept and schedule", or "needs a plan" continue.

**Gate:** do not start work on an issue that has not been accepted. Doing so is how
you end up with a PR nobody wants to merge.

## 2. Plan → an agreed plan

**Skill:** `plan-feature`
**Artefact:** a plan comment on the issue: outcome, constraints, out-of-scope,
numbered steps, risks, open questions.

Skip only when the change is a one-line fix with an understood cause. When in
doubt, write the plan — it is ten minutes.

**Gate:** open questions are answered and the plan is agreed before any edit. If
the person who could answer is unavailable, state the assumption you are proceeding
on, in the plan, so it can be corrected cheaply.

## 3. Implement → a green branch

**Skills:** `implement-change`, `write-tests`
**Artefact:** a branch whose full suite, lint and type checks pass.

One commit per plan step. Tests alongside the code, not after. If the plan turns
out to be wrong, stop and return to stage 2 — do not improvise past it and explain
afterwards.

**Gate:** the [definition of done](../docs/house-rules.md#definition-of-done),
honestly assessed. Run the commands; do not assume.

## 4. Self-review → a diff you would defend

**Skill:** `review-code`, applied to your own work
**Artefact:** a diff you have read end to end in the PR view.

Catch here what you do not want a reviewer to spend attention on: stray files,
debug output, scope creep, a test that does not assert.

## 5. Ship → a reviewable PR

**Skill:** `ship-pr`
**Artefact:** a PR whose description explains why, what changed, how it was
verified, and the risk.

Split if it is over ~400 lines of real change. Say what kind of review you want.

## 6. Review → resolved findings

**Skill:** `review-code`, by someone other than the author
**Artefact:** every finding answered; blocking findings resolved.

An agent's PR gets a human reviewer. A human's PR may get an agent reviewer, but
the accountability stays with a person.

## 7. Merge → a closed loop

**Artefact:** merged commit, issue closed with a reference, follow-ups filed as
issues, and any decision that surfaced during review written up as an ADR.

**Gate:** CI green on the current head. Not on an earlier commit.

---

## Where it goes wrong

| Symptom | Missing stage |
|---|---|
| PR nobody wants to merge | 1 — never triaged, work was not wanted |
| Built the wrong thing | 2 — no plan, or the plan was not agreed |
| Review finds correctness bugs | 3 — tests were written to pass, not to catch |
| Review spends its time on trivia | 4 — no self-review |
| Reviewer asks "why does this exist" | 5 — description restates the diff |
| Same debate again in six months | 7 — decision never recorded |

## Escalation

At any stage, stop and involve a human for: data deletion or irreversible
migration; auth, crypto or payments; a security report; conflicting requirements
with two plausible readings. See [house rules](../docs/house-rules.md).
