from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
app = (ROOT / 'app.py').read_text(encoding='utf-8')

arena_block = app.split('elif page == "Olympic Arena":', 1)[1].split('elif page == "Event Telemetry":', 1)[0]
assert 'st.selectbox(' not in arena_block, 'Olympic Arena should not use a dropdown selector.'
assert 'render_arena_event_selector(settings)' in arena_block
assert 'Run Benchmark Question' in app
assert 'Run Custom Experiment' in app
assert 'Run All 5 Benchmark Events' in app
assert 'run_all_arena_events(settings)' in app
assert 'Challenge question event' in app
for event_id in [
    'research_sprint',
    'broken_tool_relay',
    'misinformation_challenge',
    'prompt_injection_hurdle',
    'budget_marathon',
]:
    assert event_id in app

print('ARENA EVENT LAUNCHER TEST: PASS')
print('Five visible events support an editable question workspace plus direct benchmark/custom execution; no Arena dropdown.')
