# DeployPilot Architecture

**Status:** Proposed
**Version:** 0.1
**Last Updated:** 2026-10-03

---

## 1. Purpose

DeployPilot is an agentic AI platform for investigating software deployment
failures, identifying likely root causes, producing evidence-backed
diagnoses, and eventually proposing and executing approved remediation.

The project is primarily a portfolio project demonstrating practical
agentic AI engineering rather than a generic chatbot.

The architecture therefore emphasizes:

- Agent orchestration
- Tool use
- MCP integration
- Evidence-based reasoning
- Human approval
- Sandboxed execution
- Security boundaries
- Evaluation
- Observability
- Efficient context usage

---

## 2. Architectural Principles

### 2.1 Investigation before remediation

The initial system is read-only.

DeployPilot should first:

1. Gather evidence.
2. Analyze the evidence.
3. Produce a diagnosis.
4. Explain the evidence supporting that diagnosis.
5. Suggest remediation.

It must not automatically modify repositories, infrastructure, or
deployments in the initial milestone.

---

### 2.2 Deterministic code over unnecessary agents

Use normal application code when behavior can be expressed deterministically.

Use an LLM agent when the task genuinely requires:

- Reasoning
- Interpretation
- Planning
- Ambiguous diagnosis
- Evidence synthesis

Do not use an agent for simple parsing, validation, CRUD, routing, or fixed
business rules.

---

### 2.3 Minimum necessary context

The system should provide agents with the minimum context required for
correct reasoning.

Prefer:

```
targeted retrieval
→ structured evidence
→ focused reasoning
```

over:

```
entire repository
→ entire log history
→ large raw tool responses
→ unnecessary context
```

Tools should summarize and filter data before returning it to the model
whenever doing so does not remove information required for correctness.

---

### 2.4 Read and write capabilities are separate

Read-only investigation tools must be separated from side-effecting tools.

Examples of read operations:

- Read repository files
- Inspect commits
- Inspect deployment status
- Retrieve deployment logs
- Inspect metrics

Examples of side effects:

- Push commits
- Create pull requests
- Modify environment variables
- Trigger deployments
- Change infrastructure

Side-effecting capabilities require explicit authorization.

---

## 3. High-Level Architecture

```text
                         ┌──────────────────────┐
                         │      DeployPilot     │
                         │       Web UI         │
                         │  Next.js / TypeScript │
                         └──────────┬───────────┘
                                    │
                                 HTTP/API
                                    │
                         ┌──────────▼───────────┐
                         │       FastAPI        │
                         │    Application API   │
                         └──────────┬───────────┘
                                    │
                              Agent Runtime
                                    │
                         ┌──────────▼───────────┐
                         │      Google ADK      │
                         │    Investigation     │
                         │        Agent         │
                         └──────────┬───────────┘
                                    │
                   ┌────────────────┼────────────────┐
                   │                │                │
                   ▼                ▼                ▼
              GitHub MCP       Render MCP        Sandbox
                   │                │                │
                   ▼                ▼                ▼
                GitHub            Render           Docker
```

The first implementation will use only the components required for the
current milestone.

---

## 4. Frontend

### Technology

Next.js with TypeScript.

### Responsibility

The frontend is responsible for:

- Starting investigations
- Displaying investigation status
- Displaying collected evidence
- Displaying diagnosis
- Displaying suggested remediation
- Later requesting human approval for side effects

The frontend must not contain agent reasoning logic.

---

## 5. Backend

### Technology

FastAPI with Python.

### Responsibility

The backend provides:

- HTTP API
- Authentication boundary when required
- Investigation lifecycle
- Agent invocation
- Structured API responses
- Error handling
- Future persistence integration

The backend is the boundary between the UI and the agent runtime.

---

## 6. Agent Runtime

### Technology

Google Agent Development Kit (ADK).

ADK is responsible for:

- Agent definition
- Agent orchestration
- Tool integration
- Workflow execution
- State where required
- Human-in-the-loop workflows
- Evaluation

Gemini is the reasoning model used by the agents.

The application should not scatter direct Gemini API calls throughout the
codebase.

---

## 7. Model

### Primary model

Gemini 3.1 Pro.

The model is used for tasks requiring:

- Deployment failure interpretation
- Evidence synthesis
- Root-cause reasoning
- Remediation planning

Model-specific functionality should remain behind the agent/runtime layer
where practical.

---

## 8. MCP Integration

MCP is used as the integration boundary between agents and external systems.

Initial integrations:

```text
ADK Agent
   │
   ├── GitHub MCP
   │
   └── Render MCP
```

The first implementation should restrict these integrations to read-only
operations.

---

## 9. GitHub Integration

DeployPilot will use the official GitHub MCP server where appropriate.

Initial capabilities:

- Repository metadata
- File contents
- Relevant commits
- Pull request information
- Issues when relevant
- Workflow/deployment-related information when available

The initial configuration must be read-only.

No repository modification is performed by the investigation agent.

Later capabilities may include:

- Creating a branch
- Generating a patch
- Creating a pull request

These belong to a later milestone.

---

## 10. Render Integration

DeployPilot will use Render's official MCP server where appropriate.

Initial capabilities:

- Inspect services
- Inspect deployment status
- Retrieve relevant logs
- Inspect metrics when required

The initial agent must not:

- Trigger deployments
- Modify environment variables
- Modify infrastructure
- Delete resources

Write capabilities are introduced only after the investigation workflow is
reliable and human approval is implemented.

---

## 11. Sandbox

Docker-based isolation will eventually provide a controlled environment for
running generated code, tests, and diagnostic commands.

Initial MVP does not require arbitrary code execution.

Later workflow:

```text
Diagnosis
    ↓
Suggested change
    ↓
Human approval
    ↓
Sandbox
    ↓
Apply patch
    ↓
Run tests
    ↓
Collect results
    ↓
Create PR
```

Untrusted generated code must never execute directly on the developer host.

---

## 12. Data Persistence

The first MVP should avoid unnecessary persistent infrastructure.

Initial investigations may remain stateless.

Persistent storage will be introduced when the application requires:

- Users
- Projects
- Investigation history
- Agent runs
- Tool calls
- Deployment history
- Approval records
- Generated patches
- Evaluation results

PostgreSQL is the planned persistent database when that requirement is
reached.

---

## 13. Initial Investigation Workflow

The first meaningful product workflow is:

```text
User
  │
  │ Start investigation
  ▼
FastAPI
  │
  ▼
ADK Investigation Agent
  │
  ├──── GitHub MCP
  │          │
  │          └── Repository evidence
  │
  ├──── Render MCP
  │          │
  │          └── Deployment evidence
  │
  ▼
Evidence synthesis
  │
  ▼
Root-cause diagnosis
  │
  ▼
Suggested remediation
  │
  ▼
Structured investigation report
  │
  ▼
Web UI
```

The initial workflow ends with a diagnosis and recommendation.

It does not automatically modify external systems.

---

## 14. Evidence Model

Agent conclusions should be based on explicit evidence.

Conceptually:

```text
Evidence
├── source
├── type
├── timestamp
├── reference
├── relevant content
└── reliability metadata
```

The exact schema will be defined during implementation.

The agent should distinguish:

- Observed facts
- Inferences
- Hypotheses
- Recommended actions

The system must not present an inference as an observed fact.

---

## 15. Security Boundaries

The architecture contains several trust boundaries:

```text
User Input
    ↓
Application
    ↓
LLM
    ↓
Tool Output
    ↓
External Systems
    ↓
Sandbox
```

Repository contents, logs, issue comments, pull requests, and external API
responses must be treated as potentially untrusted input.

Prompt injection resistance is therefore a design requirement.

Tool permissions should follow least privilege.

---

## 16. Human-in-the-Loop

Human approval is required before side effects.

Example:

```text
Agent proposes:

"Set DATABASE_URL in Render production environment."

        ↓

User sees:
- proposed action
- reason
- evidence
- affected resource

        ↓

User approves

        ↓

Write-capable tool executes
```

The agent must not interpret silence as approval.

---

## 17. Observability

Later versions should record:

- Investigation ID
- Agent execution
- Model usage
- Tool calls
- Tool latency
- Errors
- Evidence references
- Final diagnosis
- Human approvals
- Remediation results

Observability should help answer:

> Why did the agent reach this conclusion?

and:

> What tools and evidence influenced the decision?

---

## 18. Evaluation

Agent quality must eventually be evaluated using reproducible scenarios.

Example evaluation cases:

```text
Case 1
Missing environment variable

Case 2
Dependency installation failure

Case 3
Build failure

Case 4
Runtime crash

Case 5
Port/configuration mismatch

Case 6
External service failure
```

Evaluation should measure more than whether the final answer looks plausible.

Potential metrics include:

- Root-cause accuracy
- Evidence relevance
- Tool-selection accuracy
- False-positive rate
- Unsafe-action rate
- Latency
- Token/context usage

---

## 19. MVP Scope

### MVP includes

- Web interface
- FastAPI backend
- Google ADK
- Gemini
- One investigation agent
- GitHub read-only integration
- Render read-only integration
- Structured evidence
- Evidence-backed diagnosis
- Suggested remediation
- Basic error handling

### MVP does not include

- Automatic remediation
- Automatic deployment
- Automatic repository modification
- Production code execution
- Multi-agent swarm
- PostgreSQL
- Redis
- Kubernetes
- Complex authentication
- Billing
- Multi-tenancy

Those features may be introduced in later milestones only when justified.

---

## 20. Future Milestones

### Milestone 1 — Foundation

Repository, architecture, backend/frontend skeleton, configuration,
testing, and development tooling.

### Milestone 2 — Investigation

Implement the read-only deployment investigation workflow.

### Milestone 3 — Evidence and Evaluation

Introduce structured evidence, evaluation scenarios, and quality metrics.

### Milestone 4 — Remediation Proposal

Generate concrete remediation plans without automatically executing them.

### Milestone 5 — Sandboxed Verification

Apply proposed changes inside an isolated sandbox and run tests.

### Milestone 6 — GitHub Pull Requests

Generate branches and pull requests after explicit authorization.

### Milestone 7 — Deployment Remediation

Introduce approved Render write operations.

### Milestone 8 — Persistence and Observability

Add PostgreSQL, investigation history, agent traces, metrics, and dashboards.

### Milestone 9 — Multi-Agent Workflows

Only introduce specialized agents where evaluation demonstrates that
specialization provides a measurable benefit.

---

## 21. Architecture Decision Summary

| Area                 | Decision                                     |
| -------------------- | -------------------------------------------- |
| Frontend             | Next.js + TypeScript                         |
| Backend              | FastAPI + Python                             |
| Agent runtime        | Google ADK                                   |
| Model                | Gemini 3.1 Pro                               |
| External integration | MCP                                          |
| GitHub               | Official GitHub MCP                          |
| Render               | Official Render MCP                          |
| Execution isolation  | Docker-based sandbox                         |
| Database             | PostgreSQL later                             |
| Initial agent        | Investigation agent                          |
| Initial permissions  | Read-only                                    |
| Remediation          | Human-approved, later milestone              |
| Development approach | Incremental milestones                       |
| Context strategy     | Targeted retrieval + structured tool results |

---

## 22. Guiding Principle

DeployPilot should not attempt to demonstrate every AI technology at once.

The project should demonstrate that an agent can:

1. Gather the right evidence.
2. Reason over that evidence.
3. Explain its conclusion.
4. Propose a safe action.
5. Obtain authorization.
6. Execute the action in a controlled environment.
7. Verify the result.

Every additional technology must justify its complexity by improving one of
those capabilities.
