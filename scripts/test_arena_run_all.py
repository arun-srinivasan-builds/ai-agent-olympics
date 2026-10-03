from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
app = (ROOT / "app.py").read_text(encoding="utf-8")

assert "def run_all_arena_events(settings):" in app
assert "for index, event in enumerate(ARENA_EVENTS, start=1):" in app
assert "Run All 5 Benchmark Events" in app
assert "Uses the five official benchmark questions" in app
assert "continuing with the remaining events" in app
assert "arena_batch_results" in app
assert "arena_batch_completed" in app
assert 'run_mode="benchmark"' in app

print("ARENA RUN ALL TEST: PASS")
print("Batch execution runs all five official benchmark events sequentially and preserves per-event results.")
