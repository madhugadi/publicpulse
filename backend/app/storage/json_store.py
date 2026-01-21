"""
File-based JSON storage for PublicPulse
One file per item, keyed by slug
"""
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class JSONStore:
    """Lightweight JSON file storage"""

    def __init__(self, category: str, data_dir: Path):
        """
        Args:
            category: "movies" or "gadgets"
            data_dir: Path to the category data directory
        """
        self.category = category
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save(self, slug: str, data: Dict) -> None:
        """Save item data to JSON file"""
        file_path = self.data_dir / f"{slug}.json"

        # Ensure required fields
        if "last_updated_at" not in data:
            data["last_updated_at"] = datetime.utcnow().isoformat()

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load(self, slug: str) -> Optional[Dict]:
        """Load item data from JSON file"""
        file_path = self.data_dir / f"{slug}.json"

        if not file_path.exists():
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_all(self) -> List[Dict]:
        """List all items in this category"""
        items = []

        for file_path in self.data_dir.glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    items.append(json.load(f))
            except Exception:
                continue

        # Sort by last_updated_at descending
        items.sort(
            key=lambda x: x.get("last_updated_at", ""),
            reverse=True
        )

        return items

    def exists(self, slug: str) -> bool:
        """Check if item exists"""
        file_path = self.data_dir / f"{slug}.json"
        return file_path.exists()

    def delete(self, slug: str) -> bool:
        """Delete item"""
        file_path = self.data_dir / f"{slug}.json"

        if file_path.exists():
            file_path.unlink()
            return True

        return False
