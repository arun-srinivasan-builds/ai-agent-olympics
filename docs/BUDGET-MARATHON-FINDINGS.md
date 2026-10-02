# Budget Marathon — Final Findings

## Scope

This document records the validated Event 05 result from AI Agent Olympics. Both competitors received the same model (`gpt-4.1-mini`), task, evidence packet, 180-word response limit, six-part quality gate, deterministic checks, and semantic evaluator. No tools or live web search were used.

These are descriptive findings from one controlled execution only.

## Validated Result

| Metric | OpenAI Agents SDK | Microsoft AutoGen |
|---|---:|---:|
| Run status | success | success |
| Quality gate | PASS | PASS |
| Quality checks | 6/6 | 6/6 |
| Substantive words | 100 | 113 |
| LLM requests | 1 | 1 |
| Tool calls | 0 | 0 |
| Input tokens | 494 | 494 |
| Output tokens | 171 | 206 |
| Total tokens | 665 | 700 |
| Duration | 3.557 s | 2.942 s |
| Estimated model cost | $0.00047120 | $0.00052720 |
| Deterministic checks | 5/5 | 5/5 |
| Semantic evidence support | supported | supported |

## Quality-Gated Efficiency

Both competitors passed the same six-part quality gate, so execution metrics can be compared descriptively for this run. OpenAI Agents SDK used 35 fewer total tokens and 35 fewer output tokens, with an estimated model cost about 10.6% lower. AutoGen completed in 2.942 s versus 3.557 s, about 17% faster relative to the OpenAI run time.

These are one-run observations, not universal framework claims.

## Why the Quality Gate Matters

A system is not more efficient merely because it omits the rollback threshold, deadline, next action, or risk. Budget Marathon therefore measures **efficiency at an acceptable quality level**, not raw token minimalism.

## Pricing Basis

For `gpt-4.1-mini`, the estimate uses standard rates verified on 2026-10-02:

```text
Input:  $0.40 / 1M tokens
Output: $1.60 / 1M tokens
```

Official model reference:

```text
https://developers.openai.com/api/docs/models/gpt-4.1-mini
```

Evaluator usage is excluded from competitor cost.

## Live Evidence

```text
docs/screenshots/event05-openai-budget-result.png
docs/screenshots/event05-openai-evaluation.png
docs/screenshots/event05-autogen-budget-result.png
docs/screenshots/event05-autogen-evaluation.png
```

## Event 05 Status

```text
Budget Marathon: COMPLETE
Quality gate: VALIDATED
Citation checks: VALIDATED
Semantic evidence support: VALIDATED
Token / latency measurement: VALIDATED
Cost calculation: VALIDATED
Documentation: COMPLETE
```
