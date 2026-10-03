from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
app = (ROOT / "app.py").read_text(encoding="utf-8")
responsive = (ROOT / "src" / "responsive_dashboard.py").read_text(encoding="utf-8")
premium = (ROOT / "src" / "premium_dashboard.py").read_text(encoding="utf-8")
requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")

assert "from src.responsive_dashboard import inject_responsive_dashboard_css" in app
assert "inject_responsive_dashboard_css()" in app

# Responsive CSS must load after the approved/frozen CSS layers.
assert app.index("inject_responsive_dashboard_css()") > app.index("inject_arena_event_selector_css()")

assert "@media (max-width: 1499px)" in responsive
assert "@media (max-width: 1280px)" in responsive
assert "@media (max-width: 800px)" in responsive
assert "grid-template-columns:1fr !important" in responsive
assert "grid-template-columns:repeat(4,1fr) !important" in responsive
assert "grid-template-columns:minmax(0,1fr) 155px minmax(0,1fr) !important" in responsive
assert "height:190px !important" in responsive
assert "grid-template-columns:repeat(2,1fr) !important" in responsive
assert "flex-direction:column !important" in responsive
assert 'initial_sidebar_state="locked"' in app
assert "Oct 2026" not in premium
assert "5 EVENTS COMPLETE" in premium
assert "streamlit>=1.59,<2" in requirements
assert "overflow-x:hidden !important;" in responsive
assert "max-width:100% !important;" in responsive
assert "box-sizing:border-box !important;" in responsive

# Desktop >=1500px stays frozen: there are no responsive overrides before the
# first media query in the injected style block.
style_body = responsive.split("<style>", 1)[1].split("</style>", 1)[0]
first_rule = style_body.find("@media")
assert first_rule >= 0
assert 'section[data-testid' not in style_body[:first_rule]

print("RESPONSIVE LAYOUT TEST: PASS")
print("Approved >=1500px desktop design remains unchanged; desktop sidebar is locked open and laptop breakpoints are present for 1499px, 1280px and 800px.")
