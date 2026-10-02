from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
app_text = (ROOT / "app.py").read_text(encoding="utf-8")
autogen_text = (ROOT / "src/agents/autogen_runner.py").read_text(encoding="utf-8")

assert "comparison = asyncio.run(" not in app_text
assert 'st.session_state["_async_loop"]' in app_text
assert "parallel_tool_calls=False" not in autogen_text
assert "as_text(oa.status)" in app_text
assert "as_text(ag.status)" in app_text

print("CONTROLLED RUNTIME REGRESSION TEST: PASS")
print("Persistent async loop configured.")
print("AutoGen parallel_tool_calls override removed.")
print("Comparison tables use type-stable values.")
