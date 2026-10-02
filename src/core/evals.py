from __future__ import annotations

import re

from src.core.models import DeterministicEvaluation, ToolEvidence


CITATION_PATTERN = re.compile(r"\[(\d+)\]")


def extract_citation_numbers(answer: str) -> list[int]:
    return [int(value) for value in CITATION_PATTERN.findall(answer or "")]


def run_deterministic_evaluation(
    answer: str,
    tool_calls: int,
    evidence: list[ToolEvidence],
    evidence_supplied: bool = False,
) -> DeterministicEvaluation:
    cleaned = (answer or "").strip()
    citations = extract_citation_numbers(cleaned)

    numbers_valid = bool(citations) and all(
        1 <= number <= len(evidence) for number in citations
    )

    cited_urls_listed = False
    if numbers_valid:
        cited_urls_listed = all(
            evidence[number - 1].url
            and evidence[number - 1].url in cleaned
            for number in sorted(set(citations))
        )

    return DeterministicEvaluation(
        answer_present=len(cleaned) >= 80,
        research_accessed=(tool_calls >= 1) or evidence_supplied,
        citation_marker_present=bool(citations),
        citation_numbers_valid=numbers_valid,
        cited_urls_listed=cited_urls_listed,
    )
