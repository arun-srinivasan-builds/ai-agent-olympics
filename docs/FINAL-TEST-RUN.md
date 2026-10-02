# Final Regression Test Run

Date: 2026-10-02

## `test_budget_fixture.py`

```text
BUDGET FIXTURE TEST: PASS
Four deterministic change-governance evidence items validated.
```

## `test_budget_eval.py`

```text
BUDGET EVAL TEST: PASS
Complete concise answer passes 6/6.
Cheap but incomplete answer fails the quality gate.
```

## `test_budget_pricing.py`

```text
BUDGET PRICING TEST: PASS
gpt-4.1-mini pricing calculation = $0.40 input + $1.60 output per 1M.
Unknown models correctly report pricing unavailable.
```

## `test_prompt_injection_eval.py`

```text
PROMPT INJECTION EVAL TEST: PASS
Safe rejection scores 6/6.
Attack-following answer is detected as unsafe.
```

## `test_misinformation_eval.py`

```text
MISINFORMATION EVAL TEST: PASS
Canonical rejection detected.
OpenAI-style wrapped rejection detected.
AutoGen-style wrapped rejection detected.
Actual misinformation adoption still fails.
```

## `test_evidence_eval.py`

```text
EVIDENCE EVAL TEST: PASS
Valid citation mapping detected correctly.
Missing cited URL detected correctly.
Out-of-range citation detected correctly.
```

## `test_final_status.py`

```text
FINAL EVENT STATUS TEST: PASS
All 5 Olympic events = Complete
```
