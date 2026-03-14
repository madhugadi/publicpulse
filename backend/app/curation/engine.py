"""
Rule-based curation engine for PublicPulse
NO EMBEDDINGS - keyword matching only
Phase 0 safe
"""

from typing import List, Dict
from collections import defaultdict
from app.config import BUCKET_LIMITS
from .themes import MOVIES_THEMES, GADGETS_THEMES, VEHICLES_THEMES


# ------------------------------------------------------------------
# STRONG REGIONAL / TRANSLITERATED SIGNALS (ALLOW SINGLE COMMENT)
# ------------------------------------------------------------------

STRONG_MOVIE_SIGNALS = {
    "working": [
        # English
        "blockbuster",
        "super hit",
        "hit movie",
        "worth watching",
        "repeat value",
        "full meals",

        # Indian cinema shorthand
        "mass",
        "goosebumps",
        "super",
        "super bro",
        "super brooo",

        # Telugu / Indian transliteration
        "bagundi",                 # good
        "super undi",              # very good
        "movie bagundi",
        "hit undi",
        "blockbuster undi",
        "pakka hit",
        "full meals movie",
    ],
    "concerns": [
        "flop",
        "disaster",
        "waste of money",
        "boring",
        "average",
        "not good",
    ],
}


class CurationEngine:
    """Deterministic, rule-based curation using keyword patterns"""

    def __init__(self, category: str):
        """
        Args:
            category: "movies", "gadgets", or "vehicles"
        """
        self.category = category
        if category == "movies":
            self.themes = MOVIES_THEMES
        elif category == "gadgets":
            self.themes = GADGETS_THEMES
        else:
            self.themes = VEHICLES_THEMES
        self.strong_signals = STRONG_MOVIE_SIGNALS if category == "movies" else {}

    # ------------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------------

    def curate(self, comments: List[str], actor_names: List[str] = None) -> Dict:
        """
        Curate comments into structured buckets.
        Returns buckets (curated themes) and sentiment_counts (raw comment counts per bucket).
        """
        classified = self._classify_comments(comments)

        buckets = {
            "working": self._extract_themes(classified["working"], "working", actor_names),
            "mixed": self._extract_themes(classified["mixed"], "mixed"),
            "concerns": self._extract_themes(classified["concerns"], "concerns"),
            "resonates": self._extract_themes(classified["resonates"], "resonates"),
        }

        sentiment_counts = {
            "working": len(classified["working"]),
            "mixed": len(classified["mixed"]),
            "concerns": len(classified["concerns"]),
            "resonates": len(classified["resonates"]),
        }

        return {"buckets": buckets, "sentiment_counts": sentiment_counts}

    # ------------------------------------------------------------------
    # CLASSIFICATION
    # ------------------------------------------------------------------

    def _classify_comments(self, comments: List[str]) -> Dict[str, List[str]]:
        """Classify comments into buckets using keyword scoring"""
        classified = defaultdict(list)

        for comment in comments:
            text = comment.lower()

            scores = {
                "working": self._count_matches(text, self.themes["working"]),
                "mixed": self._count_matches(text, self.themes["mixed"]),
                "concerns": self._count_matches(text, self.themes["concerns"]),
                "resonates": self._count_matches(text, self.themes["resonates"]),
            }

            if max(scores.values()) > 0:
                bucket = max(scores, key=scores.get)
                classified[bucket].append(comment)

        return classified

    def _count_matches(self, text: str, keywords: List[str]) -> int:
        """Count keyword matches in text"""
        return sum(1 for kw in keywords if kw.lower() in text)

    # ------------------------------------------------------------------
    # THEME EXTRACTION (WITH STRONG SIGNAL OVERRIDE)
    # ------------------------------------------------------------------

    def _extract_themes(
        self,
        comments: List[str],
        bucket_type: str,
        actor_names: List[str] = None
    ) -> List[str]:
        if not comments:
            return []

        keyword_counts = defaultdict(int)

        for comment in comments:
            text = comment.lower()

            # Count normal theme keywords
            for keyword in self.themes[bucket_type]:
                if keyword.lower() in text:
                    keyword_counts[keyword] += 1

            # Count strong regional signals (movies only)
            for strong_kw in self.strong_signals.get(bucket_type, []):
                if strong_kw in text:
                    keyword_counts[strong_kw] += 2  # boost

        themes = []

        for keyword, count in keyword_counts.items():
            # Allow SINGLE comment if it's a strong signal
            if (
                count >= 2
                or keyword in self.strong_signals.get(bucket_type, [])
            ):
                themes.append((keyword, count))

        if not themes:
            return []

        themes.sort(key=lambda x: x[1], reverse=True)

        max_items = BUCKET_LIMITS[bucket_type]
        results = []

        for keyword, _ in themes[:max_items]:
            results.append(self._create_theme_sentence(keyword, bucket_type))

        # Actor name enrichment (movies, working bucket only)
        if actor_names and bucket_type == "working":
            for name in actor_names[:2]:
                if len(results) < max_items:
                    results.append(f"Positive mentions of {name}'s performance")

        return results[:max_items]

    # ------------------------------------------------------------------
    # SENTENCE BUILDER (EDITORIAL SAFE)
    # ------------------------------------------------------------------

    def _create_theme_sentence(self, keyword: str, bucket_type: str) -> str:
        if bucket_type == "working":
            return f"Positive responses describe aspects such as {keyword}"
        if bucket_type == "mixed":
            return f"Mixed reactions mention {keyword}"
        if bucket_type == "concerns":
            return f"Some viewers raise concerns around {keyword}"
        if bucket_type == "resonates":
            return f"This appears to resonate with viewers interested in {keyword}"

        return keyword
