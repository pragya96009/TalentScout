"""
Manages conversation stage transitions and progress reporting.
Stage order:
  greeting → collecting_info → tech_stack → technical_questions → wrap_up → ended

"""

_PROGRESS: dict[str, int] = {
    "greeting":            10,
    "collecting_info":     30,
    "tech_stack":          55,
    "technical_questions": 80,
    "wrap_up":             95,
    "ended":              100,
}

_LABELS: dict[str, str] = {
    "greeting":            "Welcome",
    "collecting_info":     "Collecting Information",
    "tech_stack":          "Tech Stack Assessment",
    "technical_questions": "Technical Interview",
    "wrap_up":             "Wrapping Up",
    "ended":               "Screening Complete",
}


def get_stage_progress(stage: str) -> int:
    """Return the progress-bar percentage for the given stage."""
    return _PROGRESS.get(stage, 0)


def get_stage_label(stage: str) -> str:
    """Return a human-readable label for the given stage."""
    return _LABELS.get(stage, stage.replace("_", " ").title())


# ── Stage Inference ──
_WRAP_UP_SIGNALS = {
    "recruiter will", "reach out within", "2-3 business days",
    "2–3 business days", "best of luck", "thank you for your time",
    "next steps", "formal interview",
}

_TECH_Q_SIGNALS = {
    "**python**", "**javascript**", "**react**", "**django**",
    "**node**", "**sql**", "**java**", "**typescript**",
    "here are", "technical question", "let's assess", "proficiency",
    "following question",
}

_TECH_STACK_SIGNALS = {
    "tech stack", "technologies", "programming language",
    "frameworks", "databases", "tools you", "what languages",
}

_INFO_SIGNALS = {
    "email", "phone", "location", "years of experience",
    "desired position", "current role", "tell me about yourself",
}


def _recent_bot_text(messages: list[dict], n: int = 4) -> str:
    """Return the concatenated text of the last n assistant messages, lowercased."""
    bot_msgs = [m["content"] for m in messages if m["role"] == "assistant"]
    return " ".join(bot_msgs[-n:]).lower()


def infer_stage(messages: list[dict], current_stage: str) -> str:
   
    # Never retreat from a terminal state.
    if current_stage == "ended":
        return "ended"

    recent = _recent_bot_text(messages)
    assistant_count = sum(1 for m in messages if m["role"] == "assistant")

    # Detect terminal/wrap-up stage first (highest priority).
    if any(signal in recent for signal in _WRAP_UP_SIGNALS):
        return "ended"

    # Detect technical questions stage.
    if any(signal in recent for signal in _TECH_Q_SIGNALS):
        return "technical_questions"

    # Detect tech-stack probing stage.
    if any(signal in recent for signal in _TECH_STACK_SIGNALS):
        # Only advance if we haven't already passed this stage.
        if current_stage in ("greeting", "collecting_info", "tech_stack"):
            return "tech_stack"

    # Early turns: still collecting basic info.
    if assistant_count <= 1:
        return "greeting"

    if any(signal in recent for signal in _INFO_SIGNALS):
        return "collecting_info"

    # Default: stay in current stage (never regress).
    return current_stage
