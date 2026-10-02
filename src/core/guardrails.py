class InputGuardrailError(ValueError):
    pass


def validate_research_prompt(prompt: str) -> str:
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
