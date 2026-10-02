# Broken Tool Relay — Event 02

## Purpose

Measure how each agent implementation behaves when a required research tool
experiences one controlled transient failure.

This is a resilience experiment, not a search-quality experiment.

---

## Controlled Scenario

The controller first performs one shared Serper search and freezes the resulting
evidence packet.

Each competitor then receives its own identical fault-injected tool.

### Tool contract

```text
Call 1
  -> SIMULATED_TRANSIENT_ERROR
  -> HTTP 503
  -> no evidence delivered

Call 2
  -> same frozen evidence packet
  -> recovery succeeds
```

The clean minimum recovery path is therefore:

```text
2 tool calls
```

Any call after the second one is counted as unnecessary recovery overhead.

---

## What We Measure

### Recovery

- failure injected
- retry attempted
- valid evidence recovered
- number of tool calls
- unnecessary extra calls

### Efficiency

- LLM requests
- input tokens
- output tokens
- total tokens
- duration

### Answer Quality

- meaningful answer
- research tool used
- citation marker
- citation mapping
- source URL presence
- optional semantic evidence support

Evaluator cost remains separate.

---

## Fair-Test Controls

Both competitors receive:

- same user task
- same model
- same frozen evidence packet
- same simulated first-call HTTP 503
- same second-call successful evidence response
- same answer requirements
- same semantic evaluator

No competitor performs an external web search during the relay.

The controller performs the one shared external search.

---

## Interpretation

A clean recovery looks like:

```text
Failure injected       YES
Retry attempted         YES
Recovered               YES
Tool calls              2
Extra retries           0
```

Possible failure patterns:

### Stops after failure

```text
Tool calls              1
Retry attempted         NO
Recovered               NO
```

### Over-retries

```text
Tool calls              3+
Recovered               YES
Extra retries           1+
```

### Completes from memory without evidence

This should fail evidence/citation checks even if the prose looks plausible.

---

## Validation Before Live Run

```bat
python scripts\test_broken_tool_harness.py
python scripts\test_event_status.py
```

The live result should not be committed until both competitors have been run
and the measured findings are documented.


---

# Final Validation Status — 2026-10-02

Validated live result:

```text
OpenAI Agents SDK
  Recovered: YES
  Tool calls: 2
  Extra retries: 0
  Deterministic checks: 5/5
  Evidence support: SUPPORTED

Microsoft AutoGen
  Recovered: YES
  Tool calls: 2
  Extra retries: 0
  Deterministic checks: 5/5
  Evidence support: SUPPORTED
```

Event 02 is complete.

Full measured findings:

```text
docs/BROKEN-TOOL-RELAY-FINDINGS.md
```
