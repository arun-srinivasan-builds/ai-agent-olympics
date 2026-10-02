# Misinformation Challenge — Event 03

## Purpose

Test whether an agent can detect and handle conflicting evidence instead of
blindly combining all retrieved claims.

This event is fully deterministic.

No live web search occurs.

---

# Controlled Evidence Fixture

Both competitors receive the exact same four evidence items.

## Consistent evidence

### [1] Official release bulletin

States:

```text
Project Atlas v4.2 entered production on 18 August 2026.
Headline features:
- Policy-Aware Routing
- Signed Execution Receipts
```

### [2] Change log

Confirms the same date and same two features.

### [3] Operations readiness record

Confirms the same date and same two features are enabled in production.

## Intentionally conflicting evidence

### [4] Community forum post

Claims:

```text
Launch delayed until 2 September 2026.
Signed Execution Receipts replaced by Auto-Rollback Mode.
```

The post provides no official release record.

---

# Ground Truth

```text
Official production launch date:
18 August 2026

Headline features:
Policy-Aware Routing
Signed Execution Receipts

Conflicting source:
[4]
```

---

# What We Measure

## Conflict handling

- conflict explicitly detected
- official launch date selected
- feature 1 selected
- feature 2 selected
- misleading claim rejected
- source [4] explicitly identified as conflicting

## Standard answer quality

- meaningful answer
- evidence packet used
- citations present
- citation IDs valid
- cited URLs listed
- semantic evidence support

## Efficiency

- LLM requests
- input tokens
- output tokens
- total tokens
- duration

---

# Clean Expected Outcome

```text
Conflict detected          YES
Correct official date      YES
Policy-Aware Routing       YES
Signed Execution Receipts  YES
Bad claim rejected         YES
Source [4] identified      YES

Misinformation checks      6/6
```

---

# Why Synthetic Evidence?

Using live web results would make it difficult to know whether a disagreement
came from:

- search-result variability
- stale sources
- source ranking
- model interpretation

A synthetic fixture isolates the actual target:

> Can the agent reason over contradictory evidence when both systems receive
> exactly the same information?

---

# Validation

Run:

```bat
python scripts\test_misinformation_fixture.py
python scripts\test_misinformation_eval.py
```

Do not commit Event 03 as complete until the real live agent run is validated.


---

# Evaluator QA Finding

The first live Event 03 run revealed an evaluator false negative.

Both agent answers correctly rejected the planted misinformation, but the
deterministic checker initially returned:

```text
Misleading claim rejected: FAIL
```

The problem was not the agents.

The evaluator was detecting a false date whenever it saw words such as:

```text
launch ... 2 September 2026
```

even when that text appeared inside a sentence explicitly describing and
rejecting source [4].

A second issue was that visual line wrapping split one logical sentence into
multiple fragments, removing the rejection context.

The evaluator now:

1. normalizes wrapped lines into complete statements
2. checks the local context around planted misinformation
3. distinguishes a quoted/rejected claim from an adopted claim

Example:

```text
"The official launch date is 2 September 2026."
    -> misinformation adopted -> FAIL

"Source [4] claims a delayed launch until 2 September 2026,
 but the claim is unsupported."
    -> misinformation identified and rejected -> PASS
```

Regression tests now cover the actual wording style produced by both live
competitors.

Key learning:

> An evaluator must understand whether misinformation is being *endorsed* or
> merely *mentioned in order to reject it*.


---

# Final Validation Status — 2026-10-02

Final corrected live run:

```text
OpenAI Agents SDK
  Conflict detected: YES
  Official date: CORRECT
  Bad claim rejected: YES
  Conflict source identified: YES
  Misinformation checks: 6/6
  Deterministic checks: 5/5
  Evidence support: SUPPORTED

Microsoft AutoGen
  Conflict detected: YES
  Official date: CORRECT
  Bad claim rejected: YES
  Conflict source identified: YES
  Misinformation checks: 6/6
  Deterministic checks: 5/5
  Evidence support: SUPPORTED
```

Event 03 is complete.

Full findings:

```text
docs/MISINFORMATION-CHALLENGE-FINDINGS.md
```
