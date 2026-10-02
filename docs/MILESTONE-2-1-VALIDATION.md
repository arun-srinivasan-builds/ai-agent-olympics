# Milestone 2.1 Validation

## 1. Install

```bat
pip install -r requirements.txt
```

## 2. Package + environment check

```bat
python scripts\validate_setup.py
```

## 3. Deterministic evidence eval test

```bat
python scripts\test_evidence_eval.py
```

Expected:

```text
EVIDENCE EVAL TEST: PASS
Valid citation mapping detected correctly.
Missing cited URL detected correctly.
Out-of-range citation detected correctly.
```

## 4. Launch

```bat
streamlit run app.py
```

## 5. Autonomous Research test

Live Arena:

- choose `Autonomous Research`
- keep semantic evaluator enabled
- run default Python question

Verify for each framework:

- final answer
- Research Behaviour
- generated queries
- external search count
- follow-up search status
- source domains
- deterministic checks
- semantic requirement checks

## 6. Controlled Evidence test

Run the same question again with:

```text
Controlled Evidence
```

Verify:

- dashboard reports one shared external search
- shared evidence packet is used
- each competitor shows zero competitor-specific external searches
- both still invoke the evidence tool
- both receive the same evidence item count
- semantic evaluation completes independently

## 7. API accounting

Confirm competitor model calls/tokens do not change when simply displaying evaluator usage.

Evaluator call/token totals must be shown separately.

## 8. Persistence

Verify JSON files appear in:

```text
outputs/research_sprint/
```

with mode prefixes:

```text
autonomous_...
controlled_...
```

## 9. Git safety

```bat
git status
```

Confirm `.env` is not staged.

## 10. Commit

Only after both modes pass:

```bat
git add .
git commit -m "feat: add evidence-aware Research Sprint comparison"
git status
```


## Controlled Evidence Runtime Regression Check

After applying Milestone 2.1c, restart Streamlit completely and run Controlled
Evidence once.

The run is valid only if:

- no `Event loop is closed` error appears
- no `parallel_tool_calls is only allowed when tools are specified` error appears
- the Side-by-Side table renders without a PyArrow traceback
- both competitors complete and the semantic evaluator runs


---

# Final Validation Status — 2026-10-02

Validated:

- [x] Evidence deterministic eval
- [x] Cumulative evidence registry
- [x] Persistent Streamlit async loop
- [x] AutoGen model-client configuration
- [x] Type-stable Streamlit tables
- [x] Controlled Evidence direct injection design
- [x] Autonomous Research live run
- [x] Controlled Evidence live run
- [x] Semantic evaluator separation
- [x] JSON persistence
- [x] Research Sprint findings documented

Research Sprint milestone can now be committed.
