from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
app = (ROOT / "app.py").read_text(encoding="utf-8")
css = (ROOT / "src" / "premium_dashboard.py").read_text(encoding="utf-8")

assert 'key="arena_run_all_events"' in app
assert 'key=f"arena_reset_top_{question_event_id}"' in app
assert 'key=f"arena_run_selected_{question_event_id}_' in app

# Arena actions must not stretch across their columns.
for anchor in [
    'key="arena_run_all_events"',
    'key=f"arena_reset_top_{question_event_id}"',
    'key=f"arena_run_selected_{question_event_id}_',
]:
    pos = app.index(anchor)
    nearby = app[pos:pos+420]
    assert 'use_container_width=False' in nearby, anchor

assert 'V8 compact action controls' in css
assert 'height:34px' in css
assert 'width:auto' in css

print("COMPACT ARENA BUTTONS TEST: PASS")
print("Arena action buttons are compact and no longer stretch full width.")
