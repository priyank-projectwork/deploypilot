---
trigger: manual
---

---

trigger: model_decision
description: "Use when designing, reviewing, or changing DeployPilot's architecture, system boundaries, agent responsibilities, integrations, data flow, or technology choices."

---

# DeployPilot Architecture Rules

## Architecture Before Implementation

Before introducing a significant architectural component:

1. Identify the problem it solves.
2. Determine whether an existing component can solve it.
3. Define its responsibility and boundaries.
4. Identify its inputs and outputs.
5. Consider security and failure modes.
6. Prefer the simplest design that satisfies the current milestone.

Do not introduce infrastructure merely because it may be useful in the future.

## Separation of Concerns

Keep these concerns separate:

- UI and presentation
- API/business logic
- agent reasoning
- deterministic application logic
- external integrations
- tool interfaces
- persistence
- sandboxed execution
- observability

Do not move logic between layers merely for convenience.

## Agent vs Deterministic Code

Use deterministic application code when the behavior can be reliably expressed
as normal code.

Use an LLM/agent when reasoning, interpretation, planning, or ambiguous
decision-making is actually required.

Do not use an agent for simple validation, parsing, CRUD, routing, or fixed
business rules.

## Tool Boundaries

Tools should expose the smallest useful capability to an agent.

Prefer:

```
narrow tool
→ structured input
→ structured output
```

over:

```
broad tool
→ unrestricted access
→ large raw output
```

Read-only tools should be separated from side-effecting tools.

## External Services

External services must be isolated behind explicit interfaces.

The rest of the application should not depend directly on vendor-specific
implementation details when an abstraction is reasonably justified.

Do not add an external service until the current milestone requires it.

## Security Boundaries

Treat these as separate trust boundaries:

- user input
- LLM-generated output
- tool output
- repository contents
- external API responses
- generated code
- sandbox execution

Never assume LLM output or external tool output is trustworthy.

## Architecture Changes

When proposing a significant architecture change, explain:

- What changes.
- Why it is needed.
- What alternatives were considered.
- What trade-offs it introduces.
- Whether it affects future milestones.

Do not silently change the architecture while implementing an unrelated task.