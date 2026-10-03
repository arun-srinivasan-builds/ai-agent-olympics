from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / "src" / "premium_dashboard.py").read_text(encoding="utf-8")
app = (ROOT / "app.py").read_text(encoding="utf-8")

# Approved layout keeps the central decorative 1-2-3 Olympic podium.
assert "render_podium_comparison" in text
assert "podium.png" in text
assert "Olympic-style podium" in text

# Architecture identities stay clear without implying an overall framework rank.
assert "SINGLE-AGENT EXECUTION" in text
assert "MULTI-AGENT ORCHESTRATION" in text
assert "1st place" not in text.lower()
assert "2nd place" not in text.lower()
assert "first place" not in text.lower()
assert "second place" not in text.lower()

# Lower profile cards must not carry dangling overall-rank medals.
profile_source = text[text.index("def render_profiles"):text.index("def render_medal_board")]
assert "ao-profile-badge" not in profile_source
assert ">1<" not in profile_source
assert ">2<" not in profile_source

# Persistent left navigation remains part of the approved shell.
for label in [
    "Overview", "Executive Scoreboard", "Olympic Arena", "Event Telemetry",
    "Research Sprint", "Broken Tool Relay", "Misinformation", "Prompt Injection",
    "Budget Marathon", "Final Findings",
]:
    assert label in app

print("APPROVED DESIGN LOCK TEST: PASS")
print("Approved podium, architecture identities and non-misleading profile semantics are locked.")
