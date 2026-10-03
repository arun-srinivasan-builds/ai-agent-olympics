from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
dockerignore = (ROOT / ".dockerignore").read_text(encoding="utf-8")
gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

assert "FROM python:3.11-slim" in dockerfile
assert "USER appuser" in dockerfile
assert "EXPOSE 8501" in dockerfile
assert "_stcore/health" in dockerfile
assert "streamlit" in dockerfile
assert "env_file:" in compose and ".env" in compose
assert '"8501:8501"' in compose
assert ".env" in dockerignore
assert ".env" in gitignore
assert (ROOT / "docs" / "DOCKER-VPS-DEPLOYMENT.md").exists()

print("DOCKER PACKAGING TEST: PASS")
print("Python 3.11, non-root runtime, health check, env isolation and VPS deployment docs validated.")
