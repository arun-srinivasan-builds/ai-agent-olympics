from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ui = (ROOT / 'src' / 'premium_dashboard.py').read_text(encoding='utf-8')

assert 'height:auto !important' in ui
assert 'overflow:visible !important' in ui
assert 'min-height:190px !important' in ui
assert 'height:176px !important' not in ui
assert 'overflow:hidden !important' not in ui[ui.index('.ao-profile-approved{min-height:190px'):ui.index('.ao-profile-approved .ao-profile-title')]

print('PROFILE CARD VISIBILITY TEST: PASS')
print('Profile cards expand to fit all validated findings and no longer crop the final bullet.')
