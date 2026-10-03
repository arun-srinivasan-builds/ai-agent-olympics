from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
app = (ROOT / 'app.py').read_text(encoding='utf-8')
ui = (ROOT / 'src' / 'premium_dashboard.py').read_text(encoding='utf-8')

# Approved navigation is persistent and menu-driven.
for label in [
    'Overview', 'Executive Scoreboard', 'Olympic Arena', 'Event Telemetry',
    'Research Sprint', 'Broken Tool Relay', 'Misinformation', 'Prompt Injection',
    'Budget Marathon', 'Final Findings'
]:
    assert label in app

assert 'inject_approved_design_lock_css()' in app
assert '--approved-sidebar:#0B2A52' in ui
assert 'font-family:"Manrope"' in ui
assert 'The strongest story is not who ‘won’.' in ui
assert 'Live Event Flow' in ui
assert 'Event Medal Board' in ui

# Lower profile cards must not imply overall ranking.
profile_source = ui[ui.index('def render_profiles'):ui.index('def render_medal_board')]
assert 'ao-profile-badge' not in profile_source
assert '>1<' not in profile_source
assert '>2<' not in profile_source

# The central decorative podium stays, but the old stray rendering artifact is removed.
podium = Image.open(ROOT / 'assets' / 'ui' / 'podium.png').convert('RGB')
for y in range(135, podium.height):
    for x in range(0, min(28, podium.width)):
        r, g, b = podium.getpixel((x, y))
        assert r > 245 and g > 245 and b > 245

assert (ROOT / 'docs' / 'screenshots' / 'APPROVED-DESIGN-SOURCE.png').exists()

print('APPROVED DESIGN EXACT TEST: PASS')
print('Approved visual hierarchy, navigation, typography and ranking semantics are locked.')
