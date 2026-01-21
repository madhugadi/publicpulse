"""
Gadgets data adapter for PublicPulse
"""
from typing import List
from .base import DataAdapter
from app.config import GADGETS_RECENCY_DAYS


class GadgetsAdapter(DataAdapter):
    """Adapter for fetching gadget reactions from YouTube"""

    def get_search_queries(self, item_name: str) -> List[str]:
        """
        Return YouTube search queries for gadgets

        PHASE 0 LOCKED QUERIES:
        1. "<GADGET_NAME> unboxing"
        2. "<GADGET_NAME> first impressions"
        3. "<GADGET_NAME> hands on"
        4. "<GADGET_NAME> initial review"
        5. "<GADGET_NAME> issues"
        6. "<GADGET_NAME> problems"
        """
        return [
            f"{item_name} unboxing",
            f"{item_name} first impressions",
            f"{item_name} hands on",
            f"{item_name} initial review",
            f"{item_name} issues",
            f"{item_name} problems",
        ]

    def get_recency_days(self) -> int:
        """Return recency filter for gadgets (10 days)"""
        return GADGETS_RECENCY_DAYS
