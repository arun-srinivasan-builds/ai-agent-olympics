EVENTS = [
    {
        "id": "research_sprint",
        "number": "01",
        "icon": "🔎",
        "name": "Research Sprint",
        "question": "Can the agent find, validate, and explain the right answer?",
        "business_value": "Tests whether an AI system can use external evidence instead of relying only on model memory.",
        "technical_focus": ["Research", "Grounding", "Evidence quality", "Citations"],
        "status": "Ready",
    },
    {
        "id": "broken_tool_relay",
        "number": "02",
        "icon": "🔌",
        "name": "Broken Tool Relay",
        "question": "What happens when an external tool fails during the task?",
        "business_value": "Production APIs fail. This event measures whether the agent recovers safely instead of silently producing a weak answer.",
        "technical_focus": ["Tool failure", "Retry logic", "Fallback", "Resilience"],
        "status": "Ready",
    },
    {
        "id": "misinformation_challenge",
        "number": "03",
        "icon": "🕵️",
        "name": "Misinformation Challenge",
        "question": "Can the agent detect deliberately conflicting or incorrect evidence?",
        "business_value": "Enterprise AI systems must work with imperfect information and clearly communicate uncertainty.",
        "technical_focus": ["Evidence validation", "Conflict detection", "Uncertainty", "Groundedness"],
        "status": "Ready",
    },
    {
        "id": "prompt_injection_hurdle",
        "number": "04",
        "icon": "🛡️",
        "name": "Prompt Injection Hurdle",
        "question": "Can retrieved content manipulate the agent into ignoring its instructions?",
        "business_value": "External content can contain malicious instructions. This event checks whether the agent keeps trusted instructions separate from untrusted content.",
        "technical_focus": ["Prompt injection", "Input safety", "Tool safety", "Output guardrails"],
        "status": "Ready",
    },
    {
        "id": "budget_marathon",
        "number": "05",
        "icon": "💰",
        "name": "Budget Marathon",
        "question": "How efficiently can the agent complete a useful task?",
        "business_value": "A successful agent is not useful if it burns unnecessary tokens, calls, or tool operations to get there.",
        "technical_focus": ["LLM calls", "Tool calls", "Tokens", "Estimated cost"],
        "status": "Ready",
    },
]

COMPETITORS = [
    {
        "name": "OpenAI Agents SDK",
        "short_name": "OpenAI Agents",
        "status": "Integration pending",
        "description": "Agent orchestration using OpenAI Agents SDK.",
    },
    {
        "name": "Microsoft AutoGen",
        "short_name": "AutoGen",
        "status": "Integration pending",
        "description": "Multi-agent orchestration using AutoGen AgentChat.",
    },
]

FAIR_TEST_RULES = [
    "Same user task",
    "Same underlying model where framework support allows",
    "Same model settings",
    "Equivalent tools",
    "Same evidence set",
    "Same evaluation rules",
    "Same maximum recovery attempts",
]
