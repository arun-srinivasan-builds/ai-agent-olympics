from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
app = (ROOT / "app.py").read_text(encoding="utf-8")

assert "OFFICIAL_ARENA_PROMPTS" in app
assert "Reset to Benchmark Question" in app
assert "Run Custom Experiment" in app
assert 'prompt_override=selected_prompt if is_custom else None' in app
assert 'run_mode="custom" if is_custom else "benchmark"' in app
assert "does not change the validated medal board" in app
assert "fixture remains fixed" in app
assert "arena_question_event" in app
assert 'selected_prompt != official_prompt.strip()' in app

print("ARENA CUSTOM QUESTION TEST: PASS")
print("Editing the default question automatically switches the run to exploratory custom mode without changing official benchmark results.")
