from pathlib import Path
import importlib.metadata as metadata
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

packages = [
    "streamlit",
    "openai",
    "openai-agents",
    "autogen-agentchat",
    "autogen-ext",
    "httpx",
]

print("AI Agent Olympics — setup validation")
print("-" * 48)

for package in packages:
    try:
        print(f"{package}: {metadata.version(package)}")
    except metadata.PackageNotFoundError:
        print(f"{package}: NOT INSTALLED")

print("-" * 48)
print("OPENAI_API_KEY configured:", bool(os.getenv("OPENAI_API_KEY")))
print("SERPER_API_KEY configured:", bool(os.getenv("SERPER_API_KEY")))
print("AI_MODEL:", os.getenv("AI_MODEL", "gpt-4.1-mini"))
print("EVAL_MODEL:", os.getenv("EVAL_MODEL", os.getenv("AI_MODEL", "gpt-4.1-mini")))
print()
print("Secret values are never printed.")
