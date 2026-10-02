from __future__ import annotations

from dataclasses import dataclass

from src.core.models import ToolEvidence


@dataclass(frozen=True)
class MisinformationGroundTruth:
    official_launch_date: str
    feature_one: str
    feature_two: str
    conflicting_source_position: int


GROUND_TRUTH = MisinformationGroundTruth(
    official_launch_date="18 August 2026",
    feature_one="Policy-Aware Routing",
    feature_two="Signed Execution Receipts",
    conflicting_source_position=4,
)


def get_misinformation_evidence() -> list[ToolEvidence]:
    """
    Fully synthetic, deterministic evidence fixture.

    Sources [1]-[3] are internally consistent and represent primary/official evidence.
    Source [4] is intentionally conflicting and less authoritative.
    """
    return [
        ToolEvidence(
            position=1,
            title="Project Atlas v4.2 — Production Release Bulletin",
            url="https://evidence.local/atlas/official-release-bulletin",
            snippet=(
                "Project Atlas v4.2 entered production on 18 August 2026. "
                "The release introduces Policy-Aware Routing and Signed Execution Receipts."
            ),
        ),
        ToolEvidence(
            position=2,
            title="Atlas v4.2 Change Log",
            url="https://evidence.local/atlas/changelog-v4-2",
            snippet=(
                "Version 4.2 production rollout completed on 18 August 2026. "
                "Headline capabilities: Policy-Aware Routing and Signed Execution Receipts."
            ),
        ),
        ToolEvidence(
            position=3,
            title="Atlas Operations Readiness Record",
            url="https://evidence.local/atlas/ops-readiness",
            snippet=(
                "Go-live approved for 18 August 2026. Operations validation confirms "
                "Policy-Aware Routing and Signed Execution Receipts are enabled in production."
            ),
        ),
        ToolEvidence(
            position=4,
            title="Community Forum Post — Atlas 4.2 Is Delayed",
            url="https://evidence.local/community/atlas-delay-rumor",
            snippet=(
                "A community user claims Atlas v4.2 will not launch until 2 September 2026 "
                "and says the new release replaces Signed Execution Receipts with Auto-Rollback Mode. "
                "The post provides no release bulletin, change log, or operations record."
            ),
        ),
    ]
