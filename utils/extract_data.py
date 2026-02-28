"""
utils/extract_data.py
─────────────────────
Lightweight regex/heuristic extraction of structured candidate data from
the raw conversation messages.

This is a best-effort supplement to what the LLM collects — the LLM is the
primary source of truth. This module updates session_state.candidate_data
so the sidebar panel stays in sync without an extra API call.

Fixes applied vs. original:
  - Name heuristic: requires title-case AND excludes common false-positive
    phrases (experience declarations, job titles, etc.).
  - Location: no longer hard-coded to Indian cities — accepts any phrase
    that follows "based in", "located in", "from", or "living in".
  - Tech stack splitting: handles comma, slash, "and", "&", semicolons,
    newlines, and mixed separators.
  - Phone: accepts common international and domestic formats.
"""

import re
import streamlit as st

# ── Patterns ───────────────────────────────────────────────────────────────────

_EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

_PHONE_RE = re.compile(
    r"(?:\+?\d{1,3}[\s\-]?)?(?:\(?\d{2,4}\)?[\s\-]?)?\d{3,5}[\s\-]?\d{4,6}"
)

_EXPERIENCE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:\+\s*)?(?:years?|yrs?)", re.I)

# Common words that look like names but are not (two/three alphabetic words).
_FALSE_NAME_WORDS = {
    "full time", "part time", "five years", "ten years", "senior developer",
    "software engineer", "data scientist", "not sure", "dont know",
    "no idea", "i am", "i have",
}

# Separators used in tech-stack lists.
_TECH_SPLIT_RE = re.compile(r"[,/;&\n]|\band\b", re.I)

# Location trigger phrases — extract the NP that follows.
_LOCATION_RE = re.compile(
    r"(?:based in|located in|living in|from|currently in|i(?:'m| am) in)\s+([A-Za-z ,]+?)(?:\.|,|$)",
    re.I,
)


# ── Public API ────

def extract_candidate_data(messages: list[dict]) -> dict:
    """
    Scan user messages for structured candidate fields and update
    session_state.candidate_data in place.

    Parameters
    ----------
    messages : list[dict]
        Full conversation history.

    Returns
    -------
    dict
        The updated candidate_data dictionary.
    """
    data: dict = st.session_state.candidate_data.copy()

    for msg in messages:
        if msg["role"] != "user":
            continue

        text: str = msg["content"].strip()
        lower: str = text.lower()

        # ── Email ─────────
        if "email" not in data:
            match = _EMAIL_RE.search(text)
            if match:
                data["email"] = match.group()

        # ── Phone ────────
        if "phone" not in data:
            match = _PHONE_RE.search(text)
            # Require at least 10 digits to avoid matching years/dates.
            if match and len(re.sub(r"\D", "", match.group())) >= 10:
                data["phone"] = match.group().strip()

        # ── Years of Experience ─────
        if "years_experience" not in data:
            match = _EXPERIENCE_RE.search(text)
            if match:
                data["years_experience"] = f"{match.group(1)} years"

        # ── Full Name ─────
        if "full_name" not in data:
            words = text.split()
            if (
                2 <= len(words) <= 3
                and all(w.istitle() for w in words)
                and all(w.isalpha() for w in words)
                and lower not in _FALSE_NAME_WORDS
                and not any(kw in lower for kw in ("year", "engineer", "developer", "analyst"))
            ):
                data["full_name"] = text

        # ── Desired Position ──────────
        if "desired_position" not in data:
            role_keywords = [
                "developer", "engineer", "analyst", "scientist", "architect",
                "manager", "designer", "devops", "qa", "tester", "intern",
            ]
            if any(kw in lower for kw in role_keywords):
                data["desired_position"] = text

        # ── Current Location ──────────
        if "location" not in data:
            match = _LOCATION_RE.search(text)
            if match:
                data["location"] = match.group(1).strip().title()

        # ── Tech Stack ──────────
        if "tech_stack" not in data:
            tech_keywords = [
                "python", "java", "javascript", "typescript", "c++", "c#",
                "ruby", "go", "rust", "php", "swift", "kotlin",
                "react", "angular", "vue", "django", "flask", "fastapi",
                "spring", "node", "express", "rails",
                "sql", "postgres", "mysql", "mongodb", "redis", "sqlite",
                "docker", "kubernetes", "aws", "gcp", "azure",
                "git", "linux", "terraform", "graphql",
                "power bi", "tableau", "excel", "pandas", "numpy",
            ]
            if any(tech in lower for tech in tech_keywords):
                raw_items = _TECH_SPLIT_RE.split(text)
                cleaned = [item.strip() for item in raw_items if item.strip()]
                if cleaned:
                    data["tech_stack"] = cleaned

    st.session_state.candidate_data = data
    return data
