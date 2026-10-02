from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class TraceEvent:
    stage: str
    status: str
    detail: str


@dataclass
class ToolEvidence:
    position: int
    title: str
    url: str
    snippet: str


@dataclass
class ResearchBehavior:
    mode: str = "autonomous"
    queries_generated: list[str] = field(default_factory=list)
    tool_calls: int = 0
    external_search_calls: int = 0
    source_count: int = 0
    unique_domains: list[str] = field(default_factory=list)
    follow_up_search: bool = False


@dataclass
class RecoveryMetrics:
    failure_injected: bool = False
    injected_failures: int = 0
    retry_attempted: bool = False
    recovered: bool = False
    successful_evidence_returns: int = 0
    unnecessary_extra_calls: int = 0
    expected_minimum_tool_calls: int = 2


@dataclass
class MisinformationMetrics:
    conflict_detected: bool = False
    correct_launch_date_selected: bool = False
    feature_one_selected: bool = False
    feature_two_selected: bool = False
    misleading_claim_rejected: bool = False
    conflicting_source_cited_as_conflict: bool = False

    @property
    def passed_checks(self) -> int:
        return sum(
            [
                self.conflict_detected,
                self.correct_launch_date_selected,
                self.feature_one_selected,
                self.feature_two_selected,
                self.misleading_claim_rejected,
                self.conflicting_source_cited_as_conflict,
            ]
        )

    @property
    def total_checks(self) -> int:
        return 6


@dataclass
class PromptInjectionMetrics:
    injection_detected: bool = False
    trusted_severity_selected: bool = False
    trusted_action_selected: bool = False
    malicious_severity_rejected: bool = False
    attack_token_not_output: bool = False
    untrusted_source_identified: bool = False

    @property
    def passed_checks(self) -> int:
        return sum([
            self.injection_detected,
            self.trusted_severity_selected,
            self.trusted_action_selected,
            self.malicious_severity_rejected,
            self.attack_token_not_output,
            self.untrusted_source_identified,
        ])

    @property
    def total_checks(self) -> int:
        return 6

@dataclass
class DeterministicEvaluation:
    answer_present: bool = False
    research_accessed: bool = False
    citation_marker_present: bool = False
    citation_numbers_valid: bool = False
    cited_urls_listed: bool = False

    @property
    def passed_checks(self) -> int:
        return sum(
            [
                self.answer_present,
                self.research_accessed,
                self.citation_marker_present,
                self.citation_numbers_valid,
                self.cited_urls_listed,
            ]
        )

    @property
    def total_checks(self) -> int:
        return 5


@dataclass
class RequirementCheck:
    requirement: str
    status: str
    note: str


@dataclass
class SemanticEvaluation:
    status: str = "not_run"
    evidence_support: str = "not_run"
    requirements: list[RequirementCheck] = field(default_factory=list)
    unsupported_claims: list[str] = field(default_factory=list)
    contradictions: list[str] = field(default_factory=list)
    summary: str = ""
    judge_model: str = ""
    judge_requests: int = 0
    judge_input_tokens: int = 0
    judge_output_tokens: int = 0
    error: str = ""

    @property
    def incomplete_requirements(self) -> list[RequirementCheck]:
        return [
            item
            for item in self.requirements
            if item.status.lower() in {"partial", "missing"}
        ]


@dataclass
class ExecutionResult:
    framework_id: str
    framework_name: str
    event_id: str
    model: str
    mode: str
    status: str
    answer: str = ""
    duration_seconds: float = 0.0
    llm_requests: int = 0
    tool_calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    trace: list[TraceEvent] = field(default_factory=list)
    evidence: list[ToolEvidence] = field(default_factory=list)
    research_behavior: ResearchBehavior = field(default_factory=ResearchBehavior)
    recovery: RecoveryMetrics = field(default_factory=RecoveryMetrics)
    misinformation: MisinformationMetrics = field(default_factory=MisinformationMetrics)
    prompt_injection: PromptInjectionMetrics = field(default_factory=PromptInjectionMetrics)
    deterministic_eval: DeterministicEvaluation = field(
        default_factory=DeterministicEvaluation
    )
    semantic_eval: SemanticEvaluation = field(default_factory=SemanticEvaluation)
    error: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ComparisonResult:
    event_id: str
    prompt: str
    model: str
    mode: str
    openai_agents: ExecutionResult
    autogen: ExecutionResult
    created_at_utc: str
    shared_external_search_calls: int = 0
    shared_evidence: list[ToolEvidence] = field(default_factory=list)
    semantic_eval_enabled: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
