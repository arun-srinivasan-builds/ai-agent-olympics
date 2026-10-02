# Experiment Methodology — Research Sprint 2.1

## Lesson From the First Live Run

A three-check evaluator:

- answer exists
- research tool used
- citation syntax present

was too shallow.

An answer can satisfy all three and still:

- omit a requested detail
- cite a source list incompletely
- overstate what evidence establishes
- confuse preview/scheduled information with a confirmed final state

---

# Mode A — Autonomous Research

Purpose:

Evaluate the complete agent research loop.

Variables intentionally left to the competitor:

- query formulation
- number of searches
- follow-up searches
- stopping decision
- evidence selected from live search

Interpretation rule:

Different evidence is not automatically unfair here because search strategy is part of the capability being tested.

---

# Mode B — Controlled Evidence

Purpose:

Isolate evidence interpretation.

Controller:

1. performs one search
2. freezes returned evidence
3. gives the exact same evidence packet to both competitors

Interpretation rule:

Differences are less attributable to search-result variation.

---

# Deterministic Evaluation

Checks:

1. answer present
2. evidence tool accessed
3. citation marker present
4. citation numbers within captured packet
5. every cited evidence URL listed in answer

This does not prove factual correctness, but it catches citation-structure failures the original eval missed.

---

# Semantic Evidence Evaluation

A shared evaluator receives:

- user question
- evidence packet
- candidate answer

It must not use outside knowledge.

Outputs:

- evidence support
- requirement coverage
- unsupported claims
- contradictions
- summary

This is an LLM-based evaluator and therefore should be treated as another measurement instrument, not absolute truth.

---

# Evaluator Bias Limitation

Using an LLM judge introduces possible evaluator bias.

Mitigations:

- same evaluator model for both competitors
- identical evaluator instructions
- evidence packet included explicitly
- judge usage measured separately
- raw evaluation findings displayed
- no universal winner calculated

Future improvement:

Run multiple evaluator models or deterministic domain-specific assertions for critical benchmarks.

---

# Live Search Limitation

Autonomous mode uses live web search, so evidence may change between sequential runs.

Controlled Evidence exists specifically to reduce that variable.

---

# Repetition

A single run is illustrative, not statistically conclusive.

Later benchmark iterations should repeat an event several times before making claims about consistency.


---

# Controlled Evidence Final Design

Controlled Evidence does not expose a research tool to either competitor.

The controller owns the only external search.

Both competitors receive the same frozen evidence packet directly in their
input.

Therefore the intended Controlled Evidence measurements are:

```text
Shared external searches: 1
OpenAI competitor external searches: 0
AutoGen competitor external searches: 0
OpenAI evidence-tool calls: 0
AutoGen evidence-tool calls: 0
```

This design avoids meaningless repeated requests for an evidence packet that
cannot change.
