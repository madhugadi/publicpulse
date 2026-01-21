"""
Vehicles data adapter for PublicPulse
"""
from typing import List
from .base import DataAdapter
from app.config import VEHICLES_RECENCY_DAYS


class VehiclesAdapter(DataAdapter):
    """Adapter for fetching vehicle reactions from YouTube"""

    def get_search_queries(self, item_name: str) -> List[str]:
        """
        Return YouTube search queries for vehicles

        PHASE 0 LOCKED QUERIES:
        1. "<VEHICLE_NAME> first drive review"
        2. "<VEHICLE_NAME> user review"
        3. "<VEHICLE_NAME> ownership experience"
        4. "<VEHICLE_NAME> problems"
        5. "<VEHICLE_NAME> issues"
        6. "<VEHICLE_NAME> mileage"
        """
        return [
            f"{item_name} first drive review",
            f"{item_name} user review",
            f"{item_name} ownership experience",
            f"{item_name} problems",
            f"{item_name} issues",
            f"{item_name} mileage",
        ]

    def get_recency_days(self) -> int:
        """Return recency filter for vehicles (10 days)"""
        return VEHICLES_RECENCY_DAYS
