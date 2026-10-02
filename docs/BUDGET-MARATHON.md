# Budget Marathon — Event 05

## Purpose

Measure execution efficiency while holding answer quality constant.

The event avoids a common benchmark mistake:

> A shorter or cheaper answer is not more efficient if it is incomplete.

Therefore cost, tokens and latency are interpreted only after a fixed quality
gate is evaluated.

---

# Controlled Task

Both competitors receive the same four-item change-governance evidence packet.

They must produce a concise executive decision brief containing:

1. GO / NO-GO decision
2. primary risk
3. required rollback condition
4. next operational action
5. deadline
6. substantive response <= 180 words

Citations are also checked separately.

---

# Ground Truth

## Decision

```text
NO-GO
```

Reason:

```text
47 / 48 P1 tests passed.
Payment Timeout Recovery P1 test failed.
Any failed P1 gate => NO-GO.
```

## Primary Risk

```text
Payment timeout recovery can leave checkout sessions pending
and may trigger duplicate customer retries.
```

## Rollback Condition

```text
If production error rate exceeds 2.0% for five consecutive minutes:
rollback to Checkout API v8.3.
```

## Required Next Action

```text
Fix Payment Timeout Recovery defect
and rerun the payment regression suite.
```

## Deadline

```text
14:00 UTC
```

---

# Quality Gate

A run must pass all six checks:

```text
Correct decision
Primary risk present
Rollback condition present
Next action present
Deadline present
<= 180 substantive words
```

Expected:

```text
6 / 6
```

Only then should efficiency metrics be interpreted.

---

# Efficiency Metrics

- LLM requests
- tool calls
- input tokens
- output tokens
- total tokens
- duration
- estimated model cost

Evaluator calls and tokens remain separate.

---

# Cost Estimate

For `gpt-4.1-mini`, this build uses standard token rates verified on
2026-10-02:

```text
Input:  $0.40 / 1M tokens
Output: $1.60 / 1M tokens
```

Formula:

```text
estimated_cost =
    input_tokens  / 1,000,000 * 0.40
  + output_tokens / 1,000,000 * 1.60
```

The pricing table is model-specific. If `AI_MODEL` is changed to a model that
does not have an explicit configured rate, the UI reports cost as unavailable
rather than silently using the wrong price.

The estimate covers model tokens only.

---

# Fair Test Controls

Both competitors receive:

- same model
- same task
- same evidence
- same 180-word budget
- same quality gate
- no tools
- no live web search
- same semantic evaluator

This isolates framework execution overhead and response concision as much as
possible within the experiment.

---

# Interpretation

Do not declare a framework more efficient merely because it uses fewer tokens.

A meaningful efficiency comparison requires:

```text
quality gate = PASS
evidence support = acceptable
```

for both candidates.

Even after both pass, measurements from one execution should remain descriptive
rather than universal.

---

# Validation

Before the live run:

```bat
python scripts\test_budget_fixture.py
python scripts\test_budget_eval.py
python scripts\test_budget_pricing.py
python scripts\test_event05_status.py
```

Do not commit Event 05 as complete until the live result is validated.


---

# Final Validation Status — 2026-10-02

```text
OpenAI Agents SDK
  Quality gate: PASS (6/6)
  Substantive words: 100
  LLM calls: 1
  Tool calls: 0
  Total tokens: 665
  Duration: 3.557 s
  Estimated model cost: $0.00047120
  Deterministic checks: 5/5
  Evidence support: SUPPORTED

Microsoft AutoGen
  Quality gate: PASS (6/6)
  Substantive words: 113
  LLM calls: 1
  Tool calls: 0
  Total tokens: 700
  Duration: 2.942 s
  Estimated model cost: $0.00052720
  Deterministic checks: 5/5
  Evidence support: SUPPORTED
```

Event 05 is complete. See `docs/BUDGET-MARATHON-FINDINGS.md`.
