# Broken Tool Relay — Final Findings

## Scope

This document records the validated Event 02 result from the AI Agent Olympics.

The event compares how two agent implementations behave when a required
research tool experiences one deterministic transient failure.

These are descriptive findings from this experiment only.

---

# Scenario

The controller performed one shared external search and froze the evidence.

Each competitor then received an identical fault-injected tool.

```text
Tool call #1
    -> SIMULATED_TRANSIENT_ERROR
    -> HTTP 503
    -> no evidence

Tool call #2
    -> same frozen evidence packet
    -> recovery succeeds
```

The minimum clean recovery path was therefore:

```text
2 tool calls
```

Any calls beyond that were counted as unnecessary recovery overhead.

---

# Validated Result

| Metric | OpenAI Agents SDK | Microsoft AutoGen |
|---|---:|---:|
| Run status | success | success |
| Failure injected | yes | yes |
| Retry attempted | yes | yes |
| Recovered | yes | yes |
| Tool calls | 2 | 2 |
| Minimum clean path | 2 | 2 |
| Unnecessary extra calls | 0 | 0 |
| LLM requests | 3 | 3 |
| Input tokens | 1,326 | 1,290 |
| Output tokens | 128 | 125 |
| Total tokens | 1,454 | 1,415 |
| Duration | 7.274 s | 3.596 s |
| Deterministic checks | 5/5 | 5/5 |
| Semantic evidence support | supported | supported |

---

# Recovery Behaviour

## OpenAI Agents SDK

Observed sequence:

```text
Failure injected    YES
Retry attempted      YES
Recovered            YES
Tool calls           2
Extra retries        0
```

The agent detected the simulated transient error, retried once, received the
frozen evidence, and completed the task without further tool calls.

## Microsoft AutoGen

Observed sequence:

```text
Failure injected    YES
Retry attempted      YES
Recovered            YES
Tool calls           2
Extra retries        0
```

AutoGen followed the same clean recovery path.

---

# Answer Quality

Both competitors:

- waited for valid evidence before completing
- cited delivered evidence
- passed all five deterministic checks
- produced answers supported by the semantic evidence evaluator

Result:

```text
OpenAI Agents SDK    5/5 deterministic checks
AutoGen              5/5 deterministic checks

OpenAI evidence support    SUPPORTED
AutoGen evidence support   SUPPORTED
```

---

# Efficiency Observation

The recovery path itself was identical.

Measured execution differed:

```text
OpenAI Agents SDK
    1,454 total tokens
    7.274 seconds

Microsoft AutoGen
    1,415 total tokens
    3.596 seconds
```

In this single run, AutoGen used 39 fewer model tokens and completed more
quickly.

This should not be generalized into a framework-level efficiency claim from
one execution.

The important resilience finding is that **both frameworks recovered using the
minimum clean retry path**.

---

# Main Learning

The strongest Event 02 finding is:

> A transient tool failure did not cause either agent to answer from memory,
> stop prematurely, or over-retry.

Both implementations:

1. recognized the transient failure
2. retried exactly once
3. recovered valid evidence
4. completed from the recovered evidence
5. avoided unnecessary additional calls

This is the desired resilience pattern for the controlled scenario.

---

# Why This Event Matters

A tool-using agent is not production-ready merely because it can call an API
successfully.

Real systems encounter:

- HTTP 5xx failures
- rate limits
- network interruptions
- temporary provider outages
- dependency timeouts

An agent must distinguish between:

```text
"I have no evidence"
```

and:

```text
"The evidence provider failed temporarily; I should recover safely."
```

Broken Tool Relay validates that distinction in a repeatable experiment.

---

# Evaluation Design Learning

The resilience evaluation contains two independent layers.

## Recovery checks

- failure was injected
- retry occurred
- valid evidence was recovered
- no unnecessary extra tool calls occurred

## Answer checks

- meaningful answer returned
- research tool used
- citation marker present
- citations map to delivered evidence
- cited source URLs are listed

The semantic evidence evaluator then checks whether the final answer is actually
supported by the recovered evidence.

This prevents a system from receiving a resilience PASS merely because it
retried successfully.

---

# Event 02 Status

```text
Broken Tool Relay: COMPLETE
Failure injection: VALIDATED
Recovery measurement: VALIDATED
Evidence-aware eval: VALIDATED
Documentation: COMPLETE
```

Next event:

```text
🕵️ Misinformation Challenge
```
