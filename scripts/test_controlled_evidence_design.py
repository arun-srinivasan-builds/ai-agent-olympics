from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

openai_text = (ROOT / "src/agents/openai_runner.py").read_text(encoding="utf-8")
autogen_text = (ROOT / "src/agents/autogen_runner.py").read_text(encoding="utf-8")

assert "tools=tools" in openai_text
assert "tools=tools" in autogen_text
assert "tools = []" in openai_text
assert "tools = []" in autogen_text
assert "SHARED FROZEN EVIDENCE PACKET" in openai_text
assert "SHARED FROZEN EVIDENCE PACKET" in autogen_text
assert "evidence_supplied=controlled" in openai_text
assert "evidence_supplied=controlled" in autogen_text

print("CONTROLLED EVIDENCE DESIGN TEST: PASS")
print("Controlled evidence is injected directly.")
print("No competitor research tool is required in controlled mode.")
