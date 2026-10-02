# AI Agent Olympics — Final Results

## Project Status

```text
5 / 5 EVENTS COMPLETE
```

Competitors: OpenAI Agents SDK and Microsoft AutoGen AgentChat. Primary competitor model: `gpt-4.1-mini`. The project intentionally does **not** declare a universal framework winner.

## Event 01 — Research Sprint

### Autonomous Research

| Metric | OpenAI Agents SDK | Microsoft AutoGen |
|---|---:|---:|
| LLM requests | 5 | 3 |
| External searches | 4 | 2 |
| Total tokens | 5,726 | 2,292 |
| Duration | 18.978 s | 7.972 s |
| Evidence support | partial | supported |
| Incomplete requirements | 1 | 0 |

**Learning:** Same model + same search API did not mean same evidence. Different searches produced different source packets and conclusions.

### Controlled Evidence

| Metric | OpenAI Agents SDK | Microsoft AutoGen |
|---|---:|---:|
| LLM requests | 1 | 1 |
| Evidence-tool calls | 0 | 0 |
| Total tokens | 786 | 800 |
| Duration | 2.795 s | 2.055 s |
| Evidence support | partial | partial |
| Incomplete requirements | 2 | 2 |

**Learning:** When evidence was held constant, the outputs converged substantially.

## Event 02 — Broken Tool Relay

| Metric | OpenAI Agents SDK | Microsoft AutoGen |
|---|---:|---:|
| Recovered | yes | yes |
| Tool calls | 2 | 2 |
| Extra retries | 0 | 0 |
| Total tokens | 1,454 | 1,415 |
| Duration | 7.274 s | 3.596 s |
| Deterministic checks | 5/5 | 5/5 |
| Evidence support | supported | supported |

**Learning:** Both followed the minimum clean recovery path: fail → retry once → recover → answer.

## Event 03 — Misinformation Challenge

| Metric | OpenAI Agents SDK | Microsoft AutoGen |
|---|---:|---:|
| Misinformation checks | 6/6 | 6/6 |
| Total tokens | 797 | 774 |
| Duration | 4.508 s | 2.959 s |
| Deterministic checks | 5/5 | 5/5 |
| Evidence support | supported | supported |

**Learning:** Both rejected a conflicting lower-authority source. The first evaluator also produced a false negative, teaching that mentioning misinformation to reject it is not the same as adopting it.

## Event 04 — Prompt Injection Hurdle

| Metric | OpenAI Agents SDK | Microsoft AutoGen |
|---|---:|---:|
| Prompt-injection checks | 6/6 | 6/6 |
| Total tokens | 824 | 810 |
| Duration | 4.318 s | 2.612 s |
| Deterministic checks | 4/5 | 5/5 |
| Evidence support | supported | supported |

**Learning:** Both preserved trusted instruction hierarchy. OpenAI's 4/5 deterministic result was a separate citation-completeness issue, not a security failure.

## Event 05 — Budget Marathon

| Metric | OpenAI Agents SDK | Microsoft AutoGen |
|---|---:|---:|
| Quality gate | PASS | PASS |
| Quality checks | 6/6 | 6/6 |
| Substantive words | 100 | 113 |
| LLM requests | 1 | 1 |
| Input tokens | 494 | 494 |
| Output tokens | 171 | 206 |
| Total tokens | 665 | 700 |
| Duration | 3.557 s | 2.942 s |
| Estimated model cost | $0.00047120 | $0.00052720 |
| Deterministic checks | 5/5 | 5/5 |
| Evidence support | supported | supported |

**Learning:** With quality held constant, OpenAI used fewer tokens/lower estimated model cost in this run, while AutoGen completed faster.

## Cross-Event Findings

1. Agent behavior depends on orchestration and evidence acquisition, not only model choice.
2. Autonomous tests show realistic behavior; controlled tests isolate variables.
3. Tool reliability requires failure/retry experiments, not happy-path demos.
4. Evals themselves need regression tests and observability.
5. Security and output-quality dimensions should remain separate.
6. Efficiency must be quality-gated.

## Harness Engineering Lessons

The benchmark itself required fixes for cumulative evidence preservation, Streamlit asyncio lifecycle, AutoGen parameter compatibility, PyArrow table stability, controlled-evidence design, misinformation-evaluator false negatives, and semantic-evaluator prompt-injection hardening. Failed harness runs were excluded from final findings.

## Final Status

```text
Research Sprint              COMPLETE
Broken Tool Relay            COMPLETE
Misinformation Challenge     COMPLETE
Prompt Injection Hurdle      COMPLETE
Budget Marathon              COMPLETE
Documentation                COMPLETE
Guardrails                   INTEGRATED
Deterministic evals          INTEGRATED
Semantic evidence evals      INTEGRATED
Behind-the-Scenes traces     INTEGRATED
API efficiency metrics       INTEGRATED
```
