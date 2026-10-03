# AI Agent Olympics — Documentation Hub

This directory contains the detailed experiment design, findings, validation evidence, UI decisions, and deployment notes for **AI Agent Olympics**.

> The top-level [README](../README.md) is intentionally concise and portfolio-friendly. Use this page as the detailed documentation index.

## Start here

| Document | Purpose |
|---|---|
| [Final Results](FINAL-RESULTS.md) | Consolidated findings across all five Olympic events |
| [Experiment Methodology](EXPERIMENT-METHODOLOGY.md) | Fair-test rules, controls, metrics, and evaluation approach |
| [Architecture](ARCHITECTURE.md) | System architecture and experiment flow |
| [Event Status](EVENT-STATUS.md) | Completion state for all benchmark events |
| [Final Validation](FINAL-VALIDATION.md) | Final validation summary |
| [Final Test Run](FINAL-TEST-RUN.md) | Final test execution evidence |

## Olympic events

### Event 01 — Research Sprint

- [Validated findings](RESEARCH-SPRINT-FINDINGS.md)
- Focus: research strategy, evidence acquisition, citations, and controlled-evidence comparison

### Event 02 — Broken Tool Relay

- [Event design](BROKEN-TOOL-RELAY.md)
- [Validated findings](BROKEN-TOOL-RELAY-FINDINGS.md)
- Focus: transient failure detection, retry discipline, and recovery

### Event 03 — Misinformation Challenge

- [Event design](MISINFORMATION-CHALLENGE.md)
- [Validated findings](MISINFORMATION-CHALLENGE-FINDINGS.md)
- Focus: conflicting evidence, source weighting, and misinformation rejection

### Event 04 — Prompt Injection Hurdle

- [Event design](PROMPT-INJECTION-HURDLE.md)
- [Validated findings](PROMPT-INJECTION-HURDLE-FINDINGS.md)
- Focus: malicious retrieved instructions, trust hierarchy, and safe output

### Event 05 — Budget Marathon

- [Event design](BUDGET-MARATHON.md)
- [Validated findings](BUDGET-MARATHON-FINDINGS.md)
- Focus: quality-gated efficiency, tokens, latency, and estimated model cost

## Product and UI

| Document | Purpose |
|---|---|
| [Enterprise UI Upgrade](ENTERPRISE-UI-UPGRADE.md) | Approved enterprise dashboard design decisions |
| [Approved Design Source](screenshots/APPROVED-DESIGN-SOURCE.png) | Frozen visual baseline |
| [Approved Dashboard Reference](screenshots/approved-dashboard-reference.png) | Dashboard reference image |

## Deployment

| Document | Purpose |
|---|---|
| [Docker + VPS Deployment](DOCKER-VPS-DEPLOYMENT.md) | Containerization and VPS deployment guidance |

Current public deployment:

**https://ai-agent-olympics.srv1965124.hstgr.cloud**

## Validation philosophy

The project deliberately separates:

- competitor execution metrics from evaluator overhead
- deterministic checks from semantic evaluation
- autonomous research from controlled evidence
- security success from citation/output-quality issues
- validated benchmark results from exploratory custom Arena runs

The project does **not** claim a universal framework winner. Results are tied to the specific controlled experiments documented here.
