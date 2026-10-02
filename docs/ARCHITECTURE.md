# Architecture — AI Agent Olympics

## Objective

Build a framework-neutral experiment harness that can run the same controlled task against different agent orchestration implementations.

## High-Level Architecture

```text
                         AI AGENT OLYMPICS
                                |
                         Streamlit Dashboard
                                |
                        Experiment Controller
                                |
                  +-------------+-------------+
                  |                           |
          OpenAI Agents Runner          AutoGen Runner
                  |                           |
                  +-------------+-------------+
                                |
                         Shared Event Harness
                                |
             +------------------+------------------+
             |                  |                  |
          Tools            Guardrails           Evals
             |                  |                  |
             +------------------+------------------+
                                |
                         Result Normalizer
                                |
                        Evidence / Metrics
                                |
                         Dashboard Results
```

## Architecture Principle

Framework-specific logic stays inside dedicated runner adapters.

Everything else should be shared where possible:

- event inputs
- tool behavior
- injected failures
- evidence sets
- evaluation logic
- metric schema
- reporting

This reduces the risk of accidentally giving one framework a different test.

## Observability Principle

The UI may display:

- agent names
- task status
- tool invocations
- handoffs/delegations
- retries
- guardrail outcomes
- evaluation outcomes
- token/cost metadata
- timestamps/durations

The UI will **not** display hidden chain-of-thought.

## Milestone 1 Decision

No agent framework is imported yet.

Reason:

The dashboard and event contracts are established before framework-specific implementation so the benchmark does not get designed around one competitor.
