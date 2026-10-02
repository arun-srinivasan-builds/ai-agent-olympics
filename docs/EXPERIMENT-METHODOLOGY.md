# Experiment Methodology

## Purpose

AI Agent Olympics is a learning experiment.

It does not attempt to make a universal claim about any framework.

The aim is to observe how different orchestration approaches behave under equivalent controlled conditions.

## Core Controls

Each comparison should keep the following aligned where technically feasible:

- user task
- underlying model
- model settings
- tools
- evidence
- time/retry boundaries
- output requirements
- evaluation rules

Any unavoidable framework-specific difference must be documented.

## Planned Measures

### Effectiveness
- task completion
- answer correctness
- groundedness
- evidence quality
- instruction adherence

### Reliability
- tool failure detection
- retry behavior
- fallback behavior
- completion after failure
- unsupported claims

### Safety
- prompt-injection resistance
- input guardrail result
- tool input validation
- output validation
- evidence requirement

### Efficiency
- LLM calls
- tool calls
- token usage
- estimated model cost
- duplicated work
- recovery overhead

### Observability
- execution stages
- handoffs
- tool usage
- guardrail status
- evaluation status

## Result Language

Allowed:

> In this controlled event, Architecture A used fewer model calls.

Allowed:

> Architecture B recovered from the injected tool failure after two attempts.

Avoid:

> Architecture A is the best framework.

Avoid:

> Architecture B is always more reliable.

## No Synthetic Scores

The dashboard must not display fabricated performance numbers.

Before an event is executed, the result state is:

`Not Run`

This rule is part of the credibility of the project.
