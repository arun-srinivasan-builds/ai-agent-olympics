from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / 'src' / 'premium_dashboard.py').read_text(encoding='utf-8')
app = (ROOT / 'app.py').read_text(encoding='utf-8')

# No misleading hanging overall first/second ranking badges on framework profiles.
assert '<div class="ao-medal-badge">1</div>' not in text
assert '<div class="ao-medal-badge">2</div>' not in text
assert '<div class="ao-profile-badge">1</div>' not in text
assert '<div class="ao-profile-badge silver">2</div>' not in text

# Architecture identity is explicit in the approved comparison cards.
assert 'SINGLE-AGENT EXECUTION' in text
assert 'MULTI-AGENT ORCHESTRATION' in text

# The central 1-2-3 podium is a decorative Olympic motif from the approved design.
assert 'podium.png' in text
assert 'Olympic-style podium' in text
assert '1st place' not in text.lower()
assert '2nd place' not in text.lower()

# Sidebar navigation uses proper material icons and final reference sizing.
for icon in [':material/home:', ':material/bar_chart:', ':material/emoji_events:', ':material/monitoring:', ':material/description:', ':material/build:', ':material/gpp_maybe:', ':material/shield:', ':material/database:', ':material/flag:']:
    assert icon in app
assert 'font-size:22px !important' in text
assert 'width:238px !important' in text

# Existing regression protections.
assert 'titlefont=' not in text
assert 'flow_html = (' in text

print('UI SEMANTICS TEST: PASS')
print('Sidebar navigation uses readable material icons and approved fixed sizing.')
print('Competitor architecture identities are explicit without hanging overall-rank medals.')
print('Live Event Flow and Plotly syntax regressions remain protected.')
