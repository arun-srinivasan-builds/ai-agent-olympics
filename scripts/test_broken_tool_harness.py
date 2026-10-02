from pathlib import Path
import asyncio
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.models import ToolEvidence
from src.tools.fault_injection_tool import (
    FAILURE_MESSAGE,
    FaultInjectedEvidenceTool,
)


async def main():
    evidence = [
        ToolEvidence(
            position=1,
            title="Official evidence",
            url="https://example.com/official",
            snippet="A stable release is available.",
        )
    ]

    tool = FaultInjectedEvidenceTool(evidence)

    first = await tool.retrieve("latest release")
    assert "SIMULATED_TRANSIENT_ERROR" in first
    assert "503" in first
    assert tool.call_count == 1
    assert tool.delivered_evidence == []

    second = await tool.retrieve("latest release")
    assert "Official evidence" in second
    assert tool.call_count == 2
    assert len(tool.delivered_evidence) == 1

    recovery = tool.recovery_metrics()
    assert recovery.failure_injected is True
    assert recovery.retry_attempted is True
    assert recovery.recovered is True
    assert recovery.unnecessary_extra_calls == 0

    third = await tool.retrieve("latest release")
    recovery = tool.recovery_metrics()
    assert recovery.unnecessary_extra_calls == 1

    print("BROKEN TOOL HARNESS TEST: PASS")
    print("First call fails deterministically.")
    print("Second call returns frozen evidence.")
    print("Extra retries are measured.")


asyncio.run(main())
