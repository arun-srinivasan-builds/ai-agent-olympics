# Architecture — Milestone 2.1

## New Experiment Separation

Research Sprint now has two modes.

### Autonomous Research

```text
Question
   |
   +--> OpenAI Agent --> its own search queries --> evidence A
   |
   +--> AutoGen      --> its own search queries --> evidence B
```

This measures research strategy.

### Controlled Evidence

```text
Question
   |
Shared Serper search
   |
Frozen evidence packet
   |
   +--> OpenAI Agent
   |
   +--> AutoGen
```

This measures interpretation against the same evidence.

---

## Result Contract

Every framework still returns a common `ExecutionResult`.

Milestone 2.1 adds:

- `mode`
- `ResearchBehavior`
- `DeterministicEvaluation`
- `SemanticEvaluation`

This keeps framework-specific objects away from the UI.

---

## Evaluation Separation

Competitor execution metrics are one accounting boundary.

Semantic-evaluator usage is another.

The dashboard must never add judge tokens/calls to a competitor's efficiency metrics.

---

## Research Tool Boundary

`AutonomousResearchTool`

- agent query triggers live Serper call
- records queries
- records external calls
- records final evidence packet

`ControlledEvidenceTool`

- agent can request evidence
- always returns the same frozen packet
- performs no external search

`prefetch_shared_evidence`

- controller-owned
- one Serper call before competitors
- produces the frozen packet

---

## Observability

Visible:

- mode
- evidence requests
- search count
- source domains
- tool calls
- usage
- deterministic eval
- semantic eval

Not visible:

- hidden chain-of-thought
- secrets
- API keys


---

## Autonomous Evidence Registry Correction

Autonomous agents may search more than once.

The evidence layer therefore keeps a run-level registry rather than replacing
the prior packet after every search.

Rules:

1. First-seen URLs receive a stable citation ID.
2. Repeated URLs keep their original ID.
3. New URLs receive the next available ID.
4. Each tool response shows the IDs for that search's returned items.
5. Final evaluation receives the full cumulative registry.

This is necessary because an answer may legitimately cite evidence retrieved
during an earlier search.
