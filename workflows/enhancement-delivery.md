# Workflow: enhancement delivery

A change to a project that already exists. Same discipline as
[`new-project-delivery.md`](new-project-delivery.md), minus the engagement stage —
the project's purpose is already established, so what is missing is a precise
statement of *this* change.

Reached from [`../skills/route-request/SKILL.md`](../skills/route-request/SKILL.md)
path 3: the request changes behaviour in an existing codebase and does not meet
all six trivial criteria.

---

## 1. Specification → a confirmed spec

**Role:** [`business-analyst`](../roles/business-analyst/ROLE.md), turn one
**Artefact:** numbered acceptance criteria in Given/When/Then, interaction
descriptions, data shapes, out of scope, assumptions.

Different from a new project in one important way: **the analyst reads the code
first.** The existing behaviour, the tests around it, and the ADRs that explain
why it is shaped that way. A specification that contradicts the codebase, or that
reverses a recorded decision without noticing, is worse than none.

State what existing behaviour changes, and what stays the same. Callers depend on
both.

**Gate:** the user confirms the specification, specifically the acceptance criteria
and the out-of-scope list.

## 2. Issue set → work that can start

**Role:** `business-analyst`
**Artefact:** issues per [`manage-issues`](../skills/manage-issues/SKILL.md),
labelled by role, under one milestone.

**Gate:** every acceptance criterion appears in exactly one issue.

## 3. Sequencing → an ordered, assigned plan

**Role:** [`tech-lead`](../roles/tech-lead/ROLE.md)
**Artefact:** the issue set ordered, marked for parallelism, each assigned to
`principal-engineer` or `infra-engineer`.

For an enhancement the tech lead additionally checks: does this fit the existing
architecture, or does it introduce a second way of doing something the codebase
already does? If the latter, that is an [ADR](../skills/write-adr/SKILL.md), not a
detail.

## 4. Implementation → reviewed changes

**Roles:** [`principal-engineer`](../roles/principal-engineer/ROLE.md),
[`infra-engineer`](../roles/infra-engineer/ROLE.md), reviewed by `tech-lead`
**Artefact:** per issue — a merged PR with a test per acceptance criterion and
review findings resolved. Each issue runs [`issue-to-merge.md`](issue-to-merge.md).

Specific to enhancements: **do not break existing callers silently.** Search for
usages rather than assuming; a regression test for behaviour that must not change
is as valuable as a test for the new behaviour.

**Gate:** tech lead review on every change, and the full existing suite passing —
not just the new tests.

## 5. Verification → a QA report

**Role:** [`qa-engineer`](../roles/qa-engineer/ROLE.md)
**Artefact:** PASS, FAIL or BLOCKED per criterion, with steps and observations.

Plus, for an enhancement: exercise the neighbouring behaviour that was supposed to
stay the same. Most regressions live one step away from the change.

## 6. Acceptance → accept, or another cycle

**Role:** `business-analyst`, turn two
**Artefact:** a decision, per criterion.

- **All met** → stage 7.
- **Any unmet** → reopen the owning issues naming what is missing, return to
  **stage 3**. Repeat until the analyst accepts.
- **Third failed cycle on the same criterion** → stop, escalate to the user: the
  specification is the problem.

## 7. Signoff and closure

- The user signs off.
- Every issue closed with evidence — PR, criteria passed, QA report.
- Milestone closed.
- Decisions recorded as ADRs; anything found but not fixed filed as a linked issue.

---

## What is deliberately absent

**No engagement manager.** Its output — problem, users, outcomes, constraints —
already exists for this project. If you find yourself needing it, the request is
not an enhancement: it is a new project wearing one, and it should be re-routed.

Signals that you are in the wrong workflow: the analyst cannot write acceptance
criteria without asking what the product is for; the change would replace rather
than extend the existing system; or the constraints of the original project no
longer apply. Say so and re-route rather than pressing on.

## Where it goes wrong

| Symptom | Missing gate |
|---|---|
| Spec contradicts how the system works | 1 — the analyst did not read the code |
| Change lands, unrelated feature breaks | 4 — no regression test, usages not searched |
| Two ways to do the same thing now exist | 3 — the tech lead let a second pattern in |
| Passes QA, users say it is wrong | 1 — criteria confirmed by nobody |
| Work drifts far past the request | 1 — no out-of-scope list |
