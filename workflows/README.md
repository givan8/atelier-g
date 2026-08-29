# Workflows

A skill answers *how do I do X well*. A workflow answers *what is the order of
operations, and what must exist before the next step starts*.

Workflows are prose so a human can run one without tooling, and so an agent can
follow one without a runtime. Each stage names its governing skill and the artefact
that proves it is complete — the artefact is the gate, not the effort spent.

| Workflow | Use |
|---|---|
| [`issue-to-merge.md`](issue-to-merge.md) | The default path for a unit of work |
| [`new-project.md`](new-project.md) | Standing up a new repository |

## Adding one

Write a workflow when a sequence recurs, crosses more than two skills, and has a
failure mode caused by skipping a step rather than doing a step badly. If the
failure is "they did it badly", that is a skill. If it is "they never did it", that
is a workflow.

Keep the gates explicit and falsifiable. "The plan is agreed" is a gate; "the
developer understands the problem" is not.
