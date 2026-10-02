# Research Sprint — Final Findings

## Scope

These findings summarize one validated Autonomous Research run and one validated
Controlled Evidence run completed on 2026-10-02.

They are **descriptive results from this experiment only**. They are not a
universal ranking of OpenAI Agents SDK or Microsoft AutoGen.

---

# Experiment Question

```text
What is the latest stable Python 3 release, when was it released,
and what are two notable changes? Use current web evidence and cite the sources.
```

Competitor model:

```text
gpt-4.1-mini
```

Competitors:

- OpenAI Agents SDK
- Microsoft AutoGen AgentChat

---

# Experiment A — Autonomous Research

In Autonomous Research, each competitor could:

- decide what to search
- perform follow-up searches
- choose when it had enough information
- receive different live web evidence

## Measured Results

| Metric | OpenAI Agents SDK | Microsoft AutoGen |
|---|---:|---:|
| Run status | success | success |
| LLM requests | 5 | 3 |
| Evidence-tool calls | 4 | 2 |
| External searches | 4 | 2 |
| Input tokens | 5,470 | 2,107 |
| Output tokens | 256 | 185 |
| Total tokens | 5,726 | 2,292 |
| Duration | 18.978 s | 7.972 s |
| Deterministic checks | 5/5 | 5/5 |
| Semantic evidence support | partial | supported |
| Incomplete requirements | 1 | 0 |
| Evidence accumulated | 15 sources | 10 sources |

## Observed Behaviour

### OpenAI Agents SDK

The OpenAI Agents SDK competitor:

- searched four times
- accumulated 15 evidence records
- identified Python 3.14.8
- explicitly stated that the exact release date was not established by the
  evidence it had collected
- correctly cited two Python 3.14 feature changes supported by its evidence

The semantic evaluator therefore marked the answer as:

```text
Evidence support: PARTIAL
Incomplete requirements: 1
```

### Microsoft AutoGen

The AutoGen competitor:

- searched twice
- accumulated 10 evidence records
- identified Python 3.15
- supplied a release month/year
- supplied two feature changes
- produced an answer the shared evaluator considered supported by the evidence
  AutoGen had collected

The semantic evaluator therefore marked the answer as:

```text
Evidence support: SUPPORTED
Incomplete requirements: 0
```

## Important Interpretation

This does **not** establish that one framework produced the objectively correct
real-world Python answer.

The semantic evaluator answers a narrower question:

> Does the candidate answer follow from the evidence that this competitor
> actually collected?

Therefore the important Autonomous finding is:

> The two agent implementations used the same model and research API but made
> different search decisions, collected different evidence, and reached
> different conclusions.

A second important observation:

> More searches did not automatically produce a more complete answer in this
> single run.

The OpenAI Agents SDK competitor used more searches, model calls, tokens and
time, while still leaving one requested detail unresolved.

---

# Experiment B — Controlled Evidence

Controlled Evidence removes search-strategy variation.

The controller:

1. performed one external search
2. froze the resulting five-item evidence packet
3. inserted the exact same packet directly into both competitors
4. attached no competitor research tool

Expected competitor research metrics:

```text
External searches: 0
Evidence-tool calls: 0
```

## Measured Results

| Metric | OpenAI Agents SDK | Microsoft AutoGen |
|---|---:|---:|
| Run status | success | success |
| LLM requests | 1 | 1 |
| Evidence-tool calls | 0 | 0 |
| External searches | 0 | 0 |
| Input tokens | 621 | 621 |
| Output tokens | 165 | 179 |
| Total tokens | 786 | 800 |
| Duration | 2.795 s | 2.055 s |
| Deterministic checks | 5/5 | 5/5 |
| Semantic evidence support | partial | partial |
| Incomplete requirements | 2 | 2 |

Shared controller search:

```text
External searches: 1
Evidence items: 5
```

## Observed Behaviour

Both competitors interpreted the shared evidence very similarly.

Both:

- identified Python 3.14.6 based on the frozen packet
- stated that the packet did not establish an exact release date
- stated that the packet did not establish two specific notable changes
- cited the same core evidence
- completed all deterministic citation checks
- received the same semantic evidence-support result
- had the same two incomplete requirements

The token and latency differences were small relative to the Autonomous run.

---

# Main Learning

The strongest learning from Research Sprint is:

> **Same model + same tool does not mean same evidence.**

In Autonomous mode, search strategy became part of the agent behaviour.

Different queries produced different evidence, which produced different
conclusions.

When evidence was held constant in Controlled Evidence mode, the two framework
outputs converged substantially.

This single experiment therefore suggests:

> In this task, much of the observed divergence came from evidence acquisition
> and search strategy rather than from radically different interpretation of
> the same evidence.

This is a hypothesis from one controlled run, not a universal conclusion.

---

# Evaluation Learning

The project also exposed an evaluation-design lesson.

A simple evaluator checking only:

```text
Answer exists
Tool used
Citation exists
```

can produce a PASS even when:

- a requested detail is missing
- citation URLs are inconsistent
- evidence does not establish a claim
- the agent stops researching too early

The final Research Sprint evaluation therefore contains two layers.

## Deterministic

- meaningful answer
- evidence access
- citation marker
- citation number validity
- cited URL presence

## Semantic Evidence Evaluation

- requirement coverage
- evidence support
- unsupported claims
- contradictions

Evaluator model usage is recorded separately from competitor efficiency.

---

# Engineering Lessons

1. **Research strategy is part of agent behaviour.**
2. **Same research API does not guarantee same evidence.**
3. **More tool calls do not automatically mean better task completion.**
4. **Controlled evidence is needed to isolate interpretation behaviour.**
5. **Format-level evaluation is not sufficient for evidence-grounded agents.**
6. **Evaluation overhead must be kept separate from competitor API metrics.**
7. **Benchmark instrumentation must preserve all evidence seen across multiple
   searches.**
8. **A frozen evidence packet should be injected directly rather than repeatedly
   exposed through a tool that cannot return new information.**

---

# Harness Issues Found and Resolved

During development, the following benchmark-harness problems were discovered
and corrected before accepting final results:

- evidence from earlier searches was initially lost
- async event-loop lifecycle caused `Event loop is closed`
- an AutoGen `parallel_tool_calls` setting caused an invalid OpenAI request
- mixed Streamlit table types caused a PyArrow error
- Controlled Evidence repeatedly exposed the same packet through a tool,
  causing redundant calls and turn-limit failure

These failed runs were treated as implementation failures and excluded from the
final benchmark findings.

---

# Research Sprint Status

```text
Research Sprint: COMPLETE
Autonomous Research: VALIDATED
Controlled Evidence: VALIDATED
Evidence-aware eval: VALIDATED
Documentation: COMPLETE
```

Next Olympic event:

```text
🔌 Broken Tool Relay
```
