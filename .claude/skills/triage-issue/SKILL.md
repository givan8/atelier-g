---
name: triage-issue
description: >
  Use when an inbound issue, bug report or feature request needs a decision —
  what it really is, whether to do it, and what happens next. Use before
  plan-feature; most requests should be resolved here without code.
---

<!-- GENERATED FROM skills/triage-issue/SKILL.md — DO NOT EDIT. Run ./scripts/sync-harnesses.sh -->

# Triage an issue

Triage decides whether work happens, and turns a vague report into something
actionable. The most valuable outcomes are often "not doing this, here is why" and
"this is actually a different problem".

## Procedure

### 1. Classify it

- **Bug** — the system does not do what it says it does
- **Feature** — the system does what it says, and that is not enough
- **Question** — the answer is documentation, not code
- **Support** — a specific user's specific situation
- **Not our problem** — upstream dependency, misconfiguration, or by design

A surprising number of "bugs" are unwritten expectations, and a surprising number
of "features" are bugs in the documentation. Classify from what the system
promises, not from the reporter's framing.

### 2. Get it reproducible (bugs)

A bug you cannot reproduce cannot be fixed or verified. You need:

- Exact steps, or the input that triggers it
- What happened, verbatim — error text, status code, screenshot
- What was expected, and why the reporter expected it
- Environment: version, platform, configuration that differs from default

If any of these are missing, ask for them specifically. "Can you give more detail?"
gets nothing; "what was the exact error text, and what version are you on?" gets an
answer.

If it still will not reproduce, say so plainly and describe what you tried. Do not
guess at a fix for a bug you have never seen.

### 3. Find the real problem (features)

Ask what the person was trying to achieve, not what they want built. Requests
arrive pre-solutioned, and the proposed solution is often the third-best one.

Then ask whether the underlying need is already met another way. Half of feature
requests are documentation problems in disguise.

### 4. Assess honestly

- **Impact** — how many people, how often, how bad when it happens? A workaround
  existing changes this a lot.
- **Cost** — rough size, and what it commits us to maintaining afterwards. The
  ongoing cost usually exceeds the build cost.
- **Fit** — does this belong in this system at all?

Be willing to conclude the cost exceeds the value. That is a real answer.

### 5. Decide and say so

Pick one, and write the reason in the issue:

- **Fix now** — broken, and people are hitting it. Go to
  [`implement-change`](../implement-change/SKILL.md).
- **Accept, schedule** — worth doing, not now. Label it, say roughly when.
- **Needs a plan** — real but not obvious. Go to
  [`plan-feature`](../plan-feature/SKILL.md).
- **Needs information** — ask the specific questions, say what happens if there is
  no reply.
- **Won't do** — say why, in one paragraph, without hedging. Offer the workaround
  if there is one.
- **Duplicate / not our problem** — link the original or the upstream issue.

### 6. Leave the issue better than you found it

Rewrite the title to describe the problem rather than the symptom. Summarise what
was learned. A future reader — likely an agent with no other context — should
understand the state from the issue alone, without reading the whole thread.

## Escalate rather than decide

Send it to a human when the issue involves a security vulnerability, data loss or
corruption, anything affecting a specific customer's account, a legal or
compliance question, or a decision that commits the company to ongoing work.
Security reports in particular: do not discuss details in a public issue.

## Failure modes

- **Accepting everything.** A backlog where nothing is refused is a list nobody
  reads. Refusal is the point of triage.
- **Building the requested solution** instead of solving the underlying problem.
- **Fixing an unreproduced bug.** You cannot verify it, so you will not know if it
  worked.
- **The silent close.** Closing without a reason converts a reasonable decision
  into a grievance. One paragraph is enough.
- **Endless clarification.** Two rounds of questions; if it is still unclear, say
  what you would need and close it as needs-information.
