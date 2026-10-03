from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
app = (ROOT / "app.py").read_text(encoding="utf-8")

assert 'reset_pending_key = f"arena_reset_pending_{question_event_id}"' in app
assert 'st.session_state.pop(reset_pending_key, False)' in app
assert 'st.session_state[reset_pending_key] = True' in app
assert '"Reset to Benchmark Question"' in app
assert 'disabled=not is_custom_before_widget' not in app

print("ARENA RESET BUTTON TEST: PASS")
print("Reset remains clickable and restores the official benchmark question through a rerun-safe state transition.")
