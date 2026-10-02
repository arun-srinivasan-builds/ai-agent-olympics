EVENTS = [
    {
        "id": "research_sprint",
        "number": "01",
        "icon": "🔎",
        "name": "Research Sprint",
        "question": "Can the agent find, validate, and explain the right answer?",
        "business_value": "Tests research strategy, evidence interpretation, citation quality, completeness and efficiency.",
        "technical_focus": [
            "Research behaviour",
            "Grounding",
            "Citation integrity",
            "Requirement coverage",
        ],
        "status": "Live",
    },
    {
        "id": "broken_tool_relay",
        "number": "02",
        "icon": "🔌",
        "name": "Broken Tool Relay",
        "question": "What happens when an external tool fails during the task?",
        "business_value": "Production APIs fail. This event measures whether the agent recovers safely instead of silently producing a weak answer.",
        "technical_focus": ["Tool failure", "Retry logic", "Fallback", "Resilience"],
        "status": "Next",
    },
    {
        "id": "misinformation_challenge",
        "number": "03",
        "icon": "🕵️",
        "name": "Misinformation Challenge",
        "question": "Can the agent detect deliberately conflicting or incorrect evidence?",
        "business_value": "Enterprise AI systems must work with imperfect information and clearly communicate uncertainty.",
        "technical_focus": ["Evidence validation", "Conflict detection", "Uncertainty", "Groundedness"],
        "status": "Planned",
    },
    {
        "id": "prompt_injection_hurdle",
        "number": "04",
        "icon": "🛡️",
        "name": "Prompt Injection Hurdle",
        "question": "Can retrieved content manipulate the agent into ignoring its instructions?",
        "business_value": "External content can contain malicious instructions. This event checks whether the agent keeps trusted instructions separate from untrusted content.",
        "technical_focus": ["Prompt injection", "Input safety", "Tool safety", "Output guardrails"],
        "status": "Planned",
    },
    {
        "id": "budget_marathon",
        "number": "05",
        "icon": "💰",
        "name": "Budget Marathon",
        "question": "How efficiently can the agent complete a useful task?",
        "business_value": "A successful agent is not useful if it burns unnecessary tokens, calls, or tool operations to get there.",
        "technical_focus": ["LLM calls", "Tool calls", "Tokens", "Estimated cost"],
        "status": "Planned",
    },
]

COMPETITORS = [
    {
        "id": "openai_agents",
        "name": "OpenAI Agents SDK",
        "status": "Connected",
        "description": "Tool-using competitor implemented with OpenAI Agents SDK.",
    },
    {
        "id": "autogen",
        "name": "Microsoft AutoGen",
        "status": "Connected",
        "description": "Tool-using competitor implemented with AutoGen AgentChat.",
    },
]

FAIR_TEST_RULES = [
    "Same user task",
    "Same underlying OpenAI model",
    "Same shared Serper implementation",
    "Same maximum result count",
    "Same answer requirements",
    "Same deterministic evaluation rules",
    "Same semantic evaluator",
]

DEFAULT_RESEARCH_PROMPT = (
    "What is the latest stable Python 3 release, when was it released, "
    "and what are two notable changes? Use current web evidence and cite the sources."
)

RESEARCH_MODES = {
    "autonomous": {
        "label": "Autonomous Research",
        "short": "Agents choose their own searches",
        "description": (
            "Each competitor decides what to search and whether another search is needed. "
            "This tests the complete research strategy, but the evidence returned can differ."
        ),
    },
    "controlled": {
        "label": "Controlled Evidence",
        "short": "Both agents receive the same evidence",
        "description": (
            "The experiment controller performs one shared search first. Both competitors "
            "then receive exactly the same evidence packet. This isolates evidence interpretation."
        ),
    },
}
