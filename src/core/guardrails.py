from __future__ import annotations

import re

from openai import OpenAI


class InputGuardrailError(ValueError):
    """Raised when a public Arena prompt fails input-safety validation."""


PUBLIC_SAFETY_MESSAGE = (
    "This request cannot be used as an Olympic Arena experiment. "
    "Please enter a safe research or benchmarking question."
)

SAFETY_SERVICE_MESSAGE = (
    "The Arena safety check is temporarily unavailable. "
    "Please try again in a moment."
)


_SECRET_EXFILTRATION_PATTERNS = (
    re.compile(
        r"\b(?:show|reveal|print|display|dump|expose|give|return|read|extract|list)\b"
        r".{0,100}\b(?:api[\s_-]*key|secret[\s_-]*key|password|credential|access[\s_-]*token|"
        r"environment[\s_-]*variable|env[\s_-]*var|openai_api_key|serper_api_key)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:openai_api_key|serper_api_key)\b",
        re.IGNORECASE,
    ),
)

_PROMPT_OVERRIDE_PATTERNS = (
    re.compile(
        r"\b(?:ignore|disregard|override|bypass)\b.{0,100}"
        r"\b(?:previous|prior|system|developer|safety|guardrail|instructions?)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:reveal|show|print|dump|return|expose)\b.{0,100}"
        r"\b(?:system prompt|developer message|hidden instructions?|internal instructions?)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bjailbreak\b", re.IGNORECASE),
)


# Public portfolio policy is intentionally stricter than the moderation model.
# These patterns target explicit-content discovery, not legitimate sex education
# or health/wellness discussion.
_PUBLIC_EXPLICIT_CONTENT_PATTERNS = (
    re.compile(r"\bporn(?:ography|ographic|s)?\b", re.IGNORECASE),
    re.compile(r"\bxxx\b", re.IGNORECASE),
    re.compile(r"\badult\s+(?:site|sites|website|websites|video|videos|content)\b", re.IGNORECASE),
    re.compile(r"\b(?:top|best|find|show|list|recommend)\b.{0,80}\b(?:nudes?|sex\s+videos?|explicit\s+videos?)\b", re.IGNORECASE),
)


def validate_research_prompt(prompt: str) -> str:
    """Preserve the original controlled-comparison length checks."""
    cleaned = " ".join(prompt.split())

    if not cleaned:
        raise InputGuardrailError("The research question cannot be empty.")

    if len(cleaned) < 15:
        raise InputGuardrailError(
            "Use a slightly more descriptive research question (minimum 15 characters)."
        )

    if len(cleaned) > 700:
        raise InputGuardrailError(
            "Keep the Research Sprint question under 700 characters for a controlled comparison."
        )

    return cleaned


def _reject_local_attack_patterns(prompt: str) -> None:
    """Block direct secret-exfiltration and prompt-override attempts before any agent runs."""
    for pattern in _SECRET_EXFILTRATION_PATTERNS:
        if pattern.search(prompt):
            raise InputGuardrailError(PUBLIC_SAFETY_MESSAGE)

    for pattern in _PROMPT_OVERRIDE_PATTERNS:
        if pattern.search(prompt):
            raise InputGuardrailError(PUBLIC_SAFETY_MESSAGE)


    for pattern in _PUBLIC_EXPLICIT_CONTENT_PATTERNS:
        if pattern.search(prompt):
            raise InputGuardrailError(PUBLIC_SAFETY_MESSAGE)


def _moderation_flagged(prompt: str, openai_api_key: str) -> bool:
    """Classify a standalone public prompt with OpenAI's moderation endpoint."""
    if not openai_api_key:
        raise InputGuardrailError(SAFETY_SERVICE_MESSAGE)

    try:
        client = OpenAI(api_key=openai_api_key)
        response = client.moderations.create(
            model="omni-moderation-latest",
            input=prompt,
        )
        if not response.results:
            raise RuntimeError("Moderation returned no results.")
        return bool(response.results[0].flagged)
    except InputGuardrailError:
        raise
    except Exception as exc:
        # Fail closed for public custom experiments: no unmoderated input reaches the agents.
        raise InputGuardrailError(SAFETY_SERVICE_MESSAGE) from exc



def _output_requires_redaction(text: str, openai_api_key: str) -> bool:
    """Apply the same public product policy to generated custom-experiment output."""
    cleaned = " ".join((text or "").split())
    if not cleaned:
        return False

    for pattern in _PUBLIC_EXPLICIT_CONTENT_PATTERNS:
        if pattern.search(cleaned):
            return True

    return _moderation_flagged(cleaned, openai_api_key)


def sanitize_public_comparison_output(comparison, openai_api_key: str):
    """Prevent unsafe custom-run output from being displayed in the public Arena."""
    safe_message = (
        "🛡️ Output withheld by the AI Agent Olympics public-safety policy. "
        "Please use a safe research or benchmarking question."
    )

    for result in (comparison.openai_agents, comparison.autogen):
        if _output_requires_redaction(result.answer, openai_api_key):
            result.answer = safe_message
            result.status = "blocked_by_public_safety"

    return comparison

def validate_public_arena_prompt(prompt: str, openai_api_key: str) -> str:
    """Validate public custom Arena input before invoking either competitor.

    Layer 1: normalize and enforce the existing length contract.
    Layer 2: reject direct attempts to extract secrets or override trusted instructions.
    Layer 3: classify the standalone input with omni-moderation-latest.

    Official benchmark prompts do not pass through this function; only public custom runs do.
    """
    cleaned = validate_research_prompt(prompt)
    _reject_local_attack_patterns(cleaned)

    if _moderation_flagged(cleaned, openai_api_key):
        raise InputGuardrailError(PUBLIC_SAFETY_MESSAGE)

    return cleaned
