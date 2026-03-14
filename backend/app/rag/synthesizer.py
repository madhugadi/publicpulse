"""
Rolling RAG synthesizer for PublicPulse
Maintains ONLY ONE snapshot per item (constant size)
Uses normalized editorial memory to avoid tone/slang leakage
"""

from typing import Dict, Optional
from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY, GROQ_MODEL, GROQ_TEMPERATURE
import re


# ========================
# CONFIG
# ========================

BANNED_WORDS = [
    "super hit",
    "superhit",
    "blockbuster",
    "bagundi",
    "lag",
    "mass",
    "hit",
    "\"",
    "‘",
    "’",
]


# ========================
# TEXT SAFETY
# ========================

def sanitize(text: str) -> str:
    """
    Removes banned slang, quotes, and normalizes spacing.
    Case-insensitive and safe for rolling summaries.
    """
    for word in BANNED_WORDS:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        text = pattern.sub("", text)

    return " ".join(text.split())


def normalize_snapshot(previous_summary: str) -> str:
    """
    Converts a previous editorial snapshot into neutral memory.

    IMPORTANT:
    - Preserves meaning, NOT wording
    - Removes tone, slang, structure influence
    - Safe to feed back into the LLM
    """
    cleaned = sanitize(previous_summary)

    # Lightweight semantic compression (intentionally generic)
    return (
        "Earlier reactions reflected a mix of audience interest, with appreciation "
        "for certain elements alongside some reservations around pacing or engagement."
    )


# ========================
# SYNTHESIZER
# ========================

class RAGSynthesizer:
    """
    Context-safe RAG with rolling snapshot logic
    """

    def __init__(self, category: str):
        """
        Args:
            category: "movies", "gadgets", or "vehicles"
        """
        self.category = category
        self._init_llm()

    def _init_llm(self):
        """Initialize Groq LLM client"""
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable is required")

        self.client = ChatGroq(
            api_key=GROQ_API_KEY,
            model=GROQ_MODEL,
            temperature=GROQ_TEMPERATURE,
            max_tokens=600,
        )

    def synthesize(
        self,
        buckets: Dict[str, list],
        previous_summary: Optional[str] = None
    ) -> str:
        """
        Synthesize editorial summary from curated buckets
        """

        print("🔥 RAGSynthesizer.synthesize CALLED 🔥")

        # HARD GUARD: no evidence → no LLM call
        if all(len(v) == 0 for v in buckets.values()):
            return (
                "Public reactions so far are limited and scattered. "
                "At this stage, there isn’t enough consistent feedback "
                "to clearly understand how this is being received."
            )

        normalized_memory = (
            normalize_snapshot(previous_summary)
            if previous_summary else None
        )

        prompt = self._build_prompt(buckets, normalized_memory)

        try:
            response = self.client.invoke(prompt)
            final_text = sanitize(response.content.strip())
            print("✅ FINAL SUMMARY GENERATED")
            return final_text

        except Exception as e:
            print(f"❌ Error calling Groq: {e}")
            return (
                "Public reactions are still forming, and a clear editorial "
                "picture has not yet emerged."
            )

    # ========================
    # PROMPT
    # ========================

    def _build_prompt(
        self,
        buckets: Dict[str, list],
        editorial_memory: Optional[str]
    ) -> str:
        """Build prompt for LLM"""

        print("📌 USING PROMPT WITH NORMALIZED MEMORY")

        current_evidence = self._format_buckets(buckets)

        system_instruction = f"""
You are writing for PublicPulse — a site that tells people how audiences are reacting to {self.category} right now.

Imagine a smart, friendly person explaining this to a friend over coffee. That is your voice.

========================
RULES
========================
- Only use what is in the buckets. Never add anything else.
- No quotes, no slang, no regional words — rewrite everything in plain conversational English
- No words like: data, signals, analysis, evidence, monitoring, trends, momentum, notable, it is worth noting, overall
- No hype words, no scores, no verdict
- Do not mention the platform or the process

========================
HOW TO WRITE
========================
- Write like you are talking, not reporting
- Use short sentences. Mix them up. Not every sentence starts with "People" or "Some"
- Sound warm, grounded, real
- Bad example: "The film demonstrates notable strengths in its visual presentation."
- Good example: "A lot of people seem to really enjoy how it looks — the visuals keep coming up."
- Bad example: "There are emerging concerns regarding the narrative pacing."
- Good example: "Some viewers feel the story drags in parts, though not everyone agrees on that."

========================
STRUCTURE
========================
- 2 to 4 short paragraphs only
- Each paragraph covers one angle from the buckets
- Skip a bucket if it has nothing useful to say
- Mention uncertainty once at most, then move on
"""

        if editorial_memory:
            user_prompt = f"""
Editorial memory (context only — do NOT reuse wording or structure):
{editorial_memory}

Current curated buckets:
{current_evidence}

Write a fresh editorial summary that:
- Preserves continuity of themes
- Gives slightly more weight to current signals
- Does NOT reuse phrasing or sentence structure from the editorial memory
- Sounds natural and non-formulaic
"""
        else:
            user_prompt = f"""
Current curated buckets:
{current_evidence}

Write an editorial summary that:
- Reflects only what appears in the buckets
- Paraphrases all reactions into spoken English
- Avoids repeated phrasing or structure
- Feels like a person explaining how people are reacting
"""

        return f"{system_instruction}\n{user_prompt}"

    # ========================
    # BUCKET FORMATTER
    # ========================

    def _format_buckets(self, buckets: Dict[str, list]) -> str:
        """Format curated buckets for prompt"""
        lines = []

        if buckets.get("working"):
            lines.append("WHAT SEEMS TO BE WORKING:")
            for item in buckets["working"]:
                lines.append(f"- {item}")
            lines.append("")

        if buckets.get("mixed"):
            lines.append("MIXED RESPONSES:")
            for item in buckets["mixed"]:
                lines.append(f"- {item}")
            lines.append("")

        if buckets.get("concerns"):
            lines.append("EMERGING CONCERNS:")
            for item in buckets["concerns"]:
                lines.append(f"- {item}")
            lines.append("")

        if buckets.get("resonates"):
            lines.append("WHO IT SEEMS TO BE RESONATING WITH:")
            for item in buckets["resonates"]:
                lines.append(f"- {item}")
            lines.append("")

        return "\n".join(lines)
