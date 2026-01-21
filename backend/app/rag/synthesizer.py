"""
Rolling RAG synthesizer for PublicPulse
Maintains ONLY ONE snapshot per item (constant size)
"""

from typing import Dict, Optional
from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY, GROQ_MODEL, GROQ_TEMPERATURE


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


def sanitize(text: str) -> str:
    """Final safety net to remove banned words or symbols"""
    lowered = text.lower()
    for word in BANNED_WORDS:
        if word in lowered:
            text = text.replace(word, "")
    return text.strip()


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

        # HARD GUARD: no evidence → no LLM call
        if all(len(v) == 0 for v in buckets.values()):
            return (
                "Public reactions so far are limited and scattered. "
                "At this stage, there isn’t enough consistent feedback "
                "to clearly understand how this is being received."
            )

        prompt = self._build_prompt(buckets, previous_summary)

        try:
            response = self.client.invoke(prompt)
            return sanitize(response.content.strip())
        except Exception as e:
            print(f"Error calling Groq: {e}")
            return (
                "Public reactions are still forming, and a clear editorial "
                "picture has not yet emerged."
            )

    def _build_prompt(
        self,
        buckets: Dict[str, list],
        previous_summary: Optional[str]
    ) -> str:
        """Build prompt for LLM"""

        current_evidence = self._format_buckets(buckets)

        system_instruction = f"""
You are an editorial writer for PublicPulse.

PublicPulse explains how audiences are reacting RIGHT NOW to {self.category}.
It is not a review platform, not a ratings site, and not a verdict engine.

You must write like a calm, observant human editor.
Never write like an analyst, summarizer, or system.

========================
NON-NEGOTIABLE RULES
========================
- Use the curated buckets as your ONLY source of truth
- NEVER invent facts, trends, audience groups, or names
- NEVER generalize beyond what the buckets support
- NEVER repeat or quote words, slang, or phrases from the buckets
- NEVER use quotation marks of any kind
- Translate informal or regional language into neutral spoken English
- Do NOT mention data, monitoring, evidence, analysis, or signals
- Do NOT describe timelines, changes, trends, or momentum
- Do NOT reference snapshots, updates, or history
- No hype, no verdicts, no scores

STRICTLY AVOID THESE PHRASES:
- this suggests
- this indicates
- these reactions show
- overall
- on the other hand
- positive and negative
- mixed reactions
- as we continue to monitor
- early data indicates

========================
STYLE
========================
- Natural, conversational, human
- Sounds like someone explaining reactions out loud
- Short, flowing sentences
- Vary sentence openings
- Calm and grounded
- No academic or corporate language

========================
STRUCTURE
========================
- Write 2–4 short paragraphs (never more)
- Each paragraph must reflect one or more buckets
- If a bucket cannot support a paragraph, do not write one
- State uncertainty at most ONCE if truly needed, then move on
"""

        if previous_summary:
            user_prompt = f"""
Previous snapshot:
{previous_summary}

Curated buckets:
{current_evidence}

Write an updated editorial summary that:
- Gently blends both snapshots, prioritizing current reactions
- Does NOT describe comparison, change, or evolution
- Does NOT restate uncertainty unless unavoidable
- Sounds natural, human, and non-formulaic

Do not mention that multiple snapshots exist.
"""
        else:
            user_prompt = f"""
Curated buckets:
{current_evidence}

Write an editorial summary that:
- Reflects only what appears in the buckets
- Paraphrases all reactions into spoken English
- Avoids repeated phrasing or structure
- Feels like a person explaining how people are reacting

If the buckets do not support a paragraph, do not write one.
"""

        return f"{system_instruction}\n{user_prompt}"

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
