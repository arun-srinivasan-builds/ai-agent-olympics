from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
premium = (ROOT / "src" / "premium_dashboard.py").read_text(encoding="utf-8")
ui = (ROOT / "src" / "ui.py").read_text(encoding="utf-8")

for family in ["Instrument Serif", "Manrope", "IBM Plex Mono"]:
    assert family in premium, family
    assert family in ui, family

assert 'family="Manrope, Arial, sans-serif"' in premium
assert 'family="Manrope, Arial, sans-serif"' in ui

print("TYPOGRAPHY SYSTEM TEST: PASS")
print("Instrument Serif = display headings")
print("Manrope = UI/body/navigation")
print("IBM Plex Mono = metrics/code/technical labels")
