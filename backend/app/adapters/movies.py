"""
Movies data adapter for PublicPulse
"""
from typing import List
from .base import DataAdapter
from app.config import MOVIES_RECENCY_DAYS


class MoviesAdapter(DataAdapter):
    """Adapter for fetching movie audience reactions from YouTube"""

    def get_search_queries(self, item_name: str) -> List[str]:
        """
        Return YouTube search queries for movies

        PHASE 0 LOCKED QUERIES:
        1. "<MOVIE_NAME> USA premiere review"
        2. "<MOVIE_NAME> audience reaction"
        3. "<MOVIE_NAME> audience responses"
        4. "<MOVIE_NAME> first day response"
        5. "<MOVIE_NAME> public review"
        """
        return [
            f"{item_name} USA premiere review",
            f"{item_name} audience reaction",
            f"{item_name} audience responses",
            f"{item_name} first day response",
            f"{item_name} public review",
        ]

    def get_recency_days(self) -> int:
        """Return recency filter for movies (7 days)"""
        return MOVIES_RECENCY_DAYS
