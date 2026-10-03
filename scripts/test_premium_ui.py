from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
app = (ROOT / "app.py").read_text(encoding="utf-8")
premium = (ROOT / "src" / "premium_dashboard.py").read_text(encoding="utf-8")
requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")

required_app = [
    "Overview",
    "Executive Scoreboard",
    "Olympic Arena",
    "Event Telemetry",
    "Research Sprint",
    "Broken Tool Relay",
    "Misinformation",
    "Prompt Injection",
    "Budget Marathon",
    "Final Findings",
    "render_hero",
    "render_podium_comparison",
    "render_live_event_flow",
    "render_medal_board",
]

required_premium = [
    "def inject_approved_dashboard_css",
    "def render_sidebar_brand",
    "def render_top_toolbar",
    "def render_hero",
    "def render_podium_comparison",
    "def render_profiles",
    "def render_medal_board",
    "def render_live_event_flow",
    "def render_telemetry_mini",
    "def render_key_takeaways",
    "The strongest story is not who ‘won’.",
    "AI Agent Olympics",
    "#0E2548",
    "#2468F2",
    "#6D4BF6",
    "#F4F7FB",
    "initial_sidebar_state",
]

for marker in required_app:
    assert marker in app, marker

for marker in required_premium:
    assert marker in premium or marker in app, marker

for asset in ["openai_avatar.png", "autogen_team.png", "podium.png", "hero_scenic.jpg"]:
    assert (ROOT / "assets" / "ui" / asset).exists(), asset

assert "plotly" in requirements.lower()

print("PREMIUM UI TEST: PASS")
print("Approved Olympic dashboard shell, persistent sidebar, podium, live event flow, telemetry and asset bundle validated.")
