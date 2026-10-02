# Milestone 2 Validation

Use this checklist after installing Milestone 2.

---

## 1. Python Runtime

```bat
python --version
pip --version
```

Expected project baseline:

```text
Python 3.11.9
pip 26.2.1
```

---

## 2. Install

```bat
pip install -r requirements.txt
```

---

## 3. Validate Packages + Environment

```bat
python scripts\validate_setup.py
```

Expected package targets:

```text
openai-agents: 0.22.3
autogen-agentchat: 0.7.5
autogen-ext: 0.7.5
```

Expected environment status after `.env` is configured:

```text
OPENAI_API_KEY configured: True
SERPER_API_KEY configured: True
```

No secret value should appear.

---

## 4. Baseline Eval Unit Check

```bat
python scripts\test_baseline_eval.py
```

Expected:

```text
BASELINE EVAL TEST: PASS
Checks passed: 3/3
```

---

## 5. Launch

```bat
streamlit run app.py
```

---

## 6. Dashboard Checks

### Overview

Confirm:

- OpenAI Agents SDK = Connected
- Microsoft AutoGen = Connected
- Research Sprint = Live
- other events = Next / Planned
- runtime configuration = ready

### Live Arena

Use the default research prompt.

Click:

```text
Run Research Sprint
```

Expected:

- OpenAI run completes
- AutoGen run completes
- each answer contains citations
- each run reports tool calls
- each run reports token usage
- Behind-the-Scenes trace opens
- baseline evaluation opens
- captured evidence opens
- side-by-side raw metrics table appears

---

## 7. Persistence

Confirm a new file exists:

```text
outputs/research_sprint/
```

The file should contain normalized JSON results.

Do not add it to Git.

---

## 8. Git Safety

Before commit:

```bat
git status
```

Confirm `.env` is NOT staged.

Never run:

```text
git add -f .env
```

---

## 9. Commit

After successful live validation:

```bat
git add .
git commit -m "feat: add live Research Sprint agent comparison"
git status
```

Expected:

```text
nothing to commit, working tree clean
```
