# Workflow: new project delivery

From "we should build a thing" to a signed-off delivery. Six roles, five gates.

Each stage names the role that owns it and the **artefact** that must exist before
the next stage starts. The artefact is the gate — not the effort spent, not the
role's confidence. If the next role cannot start from the artefact alone, the
stage is not finished.

Reached from [`../skills/route-request/SKILL.md`](../skills/route-request/SKILL.md)
path 4. For a change to something that already exists, use
[`enhancement-delivery.md`](enhancement-delivery.md) instead.

---

## 1. Engagement → a confirmed brief

**Role:** [`engagement-manager`](../roles/engagement-manager/ROLE.md)
**Artefact:** an engagement brief — problem, users, outcomes, scope in and out,
constraints, success measures, open questions.

Questions go to the user in one batch, at most two rounds. Unanswered points
become recorded assumptions rather than a third round.

**Gate:** the user confirms the brief, specifically the out-of-scope list and the
constraints. Nothing proceeds without it.

## 2. Specification → a confirmed spec

**Role:** [`business-analyst`](../roles/business-analyst/ROLE.md), turn one
**Artefact:** numbered acceptance criteria in Given/When/Then, interaction and
screen descriptions in prose, data shapes, out of scope, assumptions.

The analyst's first job is to find what the brief left ambiguous and ask about it.
No mockup is produced — words that can be reviewed and diffed beat a picture that
cannot ([ADR-0004](../docs/adr/0004-role-based-delivery-pipeline.md)).

**Gate:** the user confirms the specification. Ask specifically about the
acceptance criteria and the out-of-scope list — those are what get corrected.

## 3. Repository and issue set → work that can start

**Roles:** `business-analyst`, with `infra-engineer` for the scaffold
**Artefacts:** a repository scaffolded per
[`scaffold-project`](../skills/scaffold-project/SKILL.md), and a set of issues per
[`manage-issues`](../skills/manage-issues/SKILL.md), labelled by role and grouped
under one milestone.

**Gate:** every acceptance criterion appears in exactly one issue, and the
scaffold's CI is green on its first commit. A scaffold that has never passed CI is
not a scaffold.

## 4. Sequencing → an ordered, assigned plan

**Role:** [`tech-lead`](../roles/tech-lead/ROLE.md)
**Artefact:** the issue set in dependency order, marked for parallelism, each
assigned to `principal-engineer` or `infra-engineer`, with reasons for the
dependencies.

Thin end-to-end slice first. Issues carrying `needs-info` do not start.

## 5. Implementation → reviewed changes

**Roles:** [`principal-engineer`](../roles/principal-engineer/ROLE.md) and
[`infra-engineer`](../roles/infra-engineer/ROLE.md), reviewed by `tech-lead`
**Artefact:** per issue — a merged pull request with a test per acceptance
criterion and the tech lead's findings resolved.

Independent issues run in parallel; dependent ones do not. Each issue follows
[`issue-to-merge.md`](issue-to-merge.md) internally.

**Gate:** tech lead review on every change. Nothing reaches QA unreviewed.

## 6. Verification → a QA report

**Role:** [`qa-engineer`](../roles/qa-engineer/ROLE.md)
**Artefact:** PASS, FAIL or BLOCKED for every acceptance criterion, each with the
steps taken and what was observed.

QA works from the specification and exercises the running system. Reading the
tests is not testing.

## 7. Acceptance → accept, or another cycle

**Role:** `business-analyst`, turn two
**Artefact:** a decision, per criterion.

- **Every criterion met** → stage 8.
- **Any criterion unmet** → the analyst reopens the owning issues naming what is
  missing, and the work returns to **stage 4**. The cycle repeats until the
  analyst accepts.

Sending back must be specific. "Needs more work" costs a full cycle; "AC4 and AC7
are unmet, the expiry path is not handled" costs an afternoon.

**Third failed cycle on the same criterion:** stop and escalate to the user. The
specification is wrong, not the implementation.

## 8. Signoff and closure

**Artefacts:**

- The user signs off. The analyst presents the work against each criterion; the
  analyst does not sign off on the user's behalf.
- Every issue is closed with its evidence — PR, criteria passed, QA report — per
  [`manage-issues`](../skills/manage-issues/SKILL.md). **An issue left open after
  signoff is the most common way this pipeline goes stale.**
- The milestone is closed.
- Decisions taken during the work are recorded as ADRs
  ([`write-adr`](../skills/write-adr/SKILL.md)).
- Anything found but not fixed exists as a new issue, linked.

---

## Where it goes wrong

| Symptom | Missing gate |
|---|---|
| Built the wrong product | 1 — no engagement, or the brief was never confirmed |
| Endless change requests after delivery | 2 — the spec was never confirmed |
| A feature nobody built | 3 — a criterion appeared in no issue |
| Parallel work that does not fit together | 4 — no sequencing, or false parallelism |
| Review finds correctness bugs | 5 — tests written to pass, not to catch |
| "It works" but it is not what was asked for | 6 — QA read the code instead of the spec |
| The same argument every cycle | 7 — send-backs were vague |
| Nobody can tell what shipped | 8 — issues closed without evidence, or left open |

## Escalation

At any stage, stop and involve the user for: data deletion, irreversible
migration, auth, cryptography, payments, access control, a security finding, or
requirements that contradict each other with two plausible readings. See
[`../docs/house-rules.md`](../docs/house-rules.md).
