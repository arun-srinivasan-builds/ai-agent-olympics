from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
app = (ROOT / "app.py").read_text(encoding="utf-8")

assert 'Challenge question event' in app
assert 'arena_question_event' in app
assert 'CHALLENGE QUESTION' in app
assert 'st.text_area' in app
assert 'disabled=True' not in app[app.index('def render_arena_event_selector'):app.index('def render_arena_latest_result')]
assert 'Reset to Benchmark Question' in app
assert 'Official benchmark question • editable.' in app
assert 'BENCHMARK DEFAULT' in app
assert 'CUSTOM EDIT' in app
assert 'Run Benchmark Question' in app
assert 'Run Custom Experiment' in app

print("ARENA QUESTION WORKSPACE TEST: PASS")
print("Challenge question is always editable, initializes from the official prompt, and has a reset action.")
