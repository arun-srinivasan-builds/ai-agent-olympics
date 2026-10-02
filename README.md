# 🏅 AI Agent Olympics

**Enterprise Agent Reliability & Efficiency Lab**

AI Agent Olympics is a controlled learning project that compares how two agent architectures behave when they face realistic operating pressure.

The first planned competitors are:

- OpenAI Agents SDK
- Microsoft AutoGen

The project is deliberately **not** a generic "which framework is better?" benchmark. It evaluates measurable behavior under the same controlled conditions.

---

## Why this project?

Most AI-agent demos show the happy path.

This project asks different questions:

- What happens when a tool fails?
- What happens when evidence conflicts?
- Can external content manipulate an agent?
- Does the architecture recover cleanly?
- How much unnecessary AI work happens along the way?
- Does a multi-agent workflow justify its extra complexity and cost?

---

## Olympic Events

### 1. 🔎 Research Sprint
Tests whether the agent can find, validate and explain an answer using external evidence.

### 2. 🔌 Broken Tool Relay
Tests whether the system can detect and recover when a required external tool fails.

### 3. 🕵️ Misinformation Challenge
Tests whether the agent notices incorrect or conflicting evidence rather than blindly accepting it.

### 4. 🛡️ Prompt Injection Hurdle
Tests whether untrusted retrieved content can override trusted agent instructions.

### 5. 💰 Budget Marathon
Tests whether the architecture completes a useful task without unnecessary model/tool calls and cost.

---

## Fair-Test Protocol

The experiment is designed around the following controls:

1. Same user task
2. Same underlying model where framework support allows
3. Same model settings
4. Equivalent tools
5. Same evidence set
6. Same evaluation rules
7. Same maximum recovery attempts

Results will be described as **measured behavior in this experiment**, not as proof that one framework is universally better.

---

## Current Status

### Milestone 1 — Dashboard & Experiment Foundation

Completed:

- [x] Enterprise dashboard shell
- [x] Five event definitions
- [x] Competitor placeholders
- [x] Fair-test protocol
- [x] Live Arena shell
- [x] Results shell
- [x] Learning log
- [x] No simulated benchmark scores

Not yet implemented:

- [ ] OpenAI Agents SDK runner
- [ ] AutoGen runner
- [ ] Shared tool harness
- [ ] Shared result schema
- [ ] Guardrail execution
- [ ] Evaluation engine
- [ ] Token/cost collection
- [ ] Event persistence
- [ ] Docker deployment
- [ ] VPS deployment

---

## Project Structure

```text
ai-agent-olympics/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── config/
│   └── events.py
├── src/
│   └── ui.py
├── docs/
│   ├── ARCHITECTURE.md
│   └── EXPERIMENT-METHODOLOGY.md
└── assets/
```

---

## Local Setup

Recommended: Python 3.11 or 3.12.

### Windows

```bat
mkdir D:\ai-agent-olympics
cd /d D:\ai-agent-olympics

python -m venv .venv
.venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt

streamlit run app.py
```

The application should open at:

```text
http://localhost:8501
```

---

## Milestone 1 Validation

Expected behavior:

- Dashboard loads without an API key.
- Overview shows five configured events.
- Events Executed remains `0 / 5`.
- Results show `Not Run` rather than placeholder scores.
- Both competitors show `Integration pending`.
- Live Arena allows selecting an event but does not execute a simulated benchmark.

---

## Documentation Strategy

This README is updated continuously throughout the build.

Each engineering milestone will document:

- architecture decisions
- new files/components
- commands and setup
- experiment definitions
- testing and validation
- errors and resolutions
- guardrails
- evaluations
- observability
- API efficiency
- benchmark evidence
- Docker/VPS deployment
- final learnings and limitations

---

## Next Milestone

**Milestone 2 — Real Agent Runners**

1. Add OpenAI Agents SDK.
2. Add AutoGen.
3. Define a common execution/result contract.
4. Run one baseline task through both implementations.
5. Capture real model/tool metrics.
6. Surface summarized execution traces in Live Arena.
