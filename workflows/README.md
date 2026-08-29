# Workflows

A skill answers *how do I do X well*. A role answers *who owns this and what may
they decide*. A workflow answers *what is the order, and what must exist before
the next stage starts*.

Workflows are prose so a human can run one without tooling, and so an agent can
follow one without a runtime. Each stage names its governing role and the artefact
that proves it is complete — the artefact is the gate, not the effort spent.

| Workflow | Use |
|---|---|
| [`new-project-delivery.md`](new-project-delivery.md) | A new product or service. Six roles, five gates, starting with engagement. |
| [`enhancement-delivery.md`](enhancement-delivery.md) | A change to something that exists. Same, minus engagement. |
| [`issue-to-merge.md`](issue-to-merge.md) | One issue, inside the implementation stage of either pipeline. |
| [`new-project.md`](new-project.md) | Standing up the repository itself — mechanics, not delivery. |

Every request enters through
[`../skills/route-request/SKILL.md`](../skills/route-request/SKILL.md), which
chooses between these and the two paths that use none of them: answering a
question, and the fast path for genuinely trivial changes.

## How they nest

```
route-request
  ├── answer                    (no workflow)
  ├── trivial change            implement-change → ship-pr
  ├── enhancement-delivery ─┐
  └── new-project-delivery ─┴── implementation stage runs issue-to-merge per issue
                                new-project-delivery stage 3 runs new-project.md
```

## Adding one

Write a workflow when a sequence recurs, crosses more than two roles or skills,
and has a failure mode caused by *skipping* a step rather than doing one badly. If
the failure is "they did it badly", that is a skill. If it is "they never did it",
that is a workflow.

Keep the gates falsifiable. "The specification is confirmed by the user" is a
gate; "the analyst understands the problem" is not.
