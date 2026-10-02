from __future__ import annotations

from src.core.models import RecoveryMetrics, ResearchBehavior, ToolEvidence
from src.tools.research_tool import format_evidence, unique_domains


FAILURE_MESSAGE = """
SIMULATED_TRANSIENT_ERROR
HTTP 503: research provider temporarily unavailable.
This is a controlled transient failure in the AI Agent Olympics.
Retry the research tool. Do not answer from memory.
""".strip()


class FaultInjectedEvidenceTool:
    """
    Deterministic Broken Tool Relay harness.

    Call 1:
        returns a simulated transient 503 failure.

    Call 2+:
        returns the same frozen evidence packet.

    No competitor-specific external web search occurs.
    """

    def __init__(
        self,
        evidence: list[ToolEvidence],
        failures_before_success: int = 1,
    ) -> None:
        self.evidence_packet = list(evidence)
        self.delivered_evidence: list[ToolEvidence] = []
        self.failures_before_success = failures_before_success

        self.call_count = 0
        self.injected_failures = 0
        self.successful_returns = 0
        self.queries: list[str] = []

    async def retrieve(self, query: str) -> str:
        self.call_count += 1
        self.queries.append(query)

        if self.injected_failures < self.failures_before_success:
            self.injected_failures += 1
            return FAILURE_MESSAGE

        self.successful_returns += 1
        self.delivered_evidence = list(self.evidence_packet)
        return format_evidence(self.delivered_evidence)

    def recovery_metrics(self) -> RecoveryMetrics:
        minimum_calls = self.failures_before_success + 1
        retry_attempted = self.call_count > self.injected_failures
        recovered = self.successful_returns > 0 and retry_attempted

        return RecoveryMetrics(
            failure_injected=self.injected_failures > 0,
            injected_failures=self.injected_failures,
            retry_attempted=retry_attempted,
            recovered=recovered,
            successful_evidence_returns=self.successful_returns,
            unnecessary_extra_calls=max(0, self.call_count - minimum_calls),
            expected_minimum_tool_calls=minimum_calls,
        )

    def behavior(self) -> ResearchBehavior:
        return ResearchBehavior(
            mode="broken_tool_relay",
            queries_generated=list(self.queries),
            tool_calls=self.call_count,
            external_search_calls=0,
            source_count=len(self.delivered_evidence),
            unique_domains=unique_domains(self.delivered_evidence),
            follow_up_search=self.call_count > 1,
        )
