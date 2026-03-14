"""
Shared ingestion function for PublicPulse Phase 0

This module contains the core ingestion logic that can be called from:
- CLI: app/scripts/run_ingestion.py
- FastAPI: POST /admin/run-ingestion

Workflow:
1. Read titles from backend/data/input/items.json
2. Loop through movies and gadgets independently
3. For each item:
   - Fetch YouTube comments via category adapter
   - Curate into buckets using rule-based engine
   - Synthesize summary using RAG (with rolling snapshot)
   - Save to JSON storage
"""
import json
import re
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from app.config import MOVIES_DIR, GADGETS_DIR, VEHICLES_DIR, TMDB_API_KEY, TMDB_BASE_URL, TMDB_IMAGE_BASE_URL
from app.adapters import MoviesAdapter, GadgetsAdapter, VehiclesAdapter
from app.curation import CurationEngine
from app.rag import RAGSynthesizer
from app.storage import JSONStore


# Input file path
INPUT_FILE = Path(__file__).parent.parent.parent / "data" / "input" / "items.json"


def run_ingestion() -> Dict[str, Any]:
    """
    Run ingestion for all items in items.json

    Returns:
        Dict with results for movies and gadgets
    """
    # Read input file
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}\n"
            f"Please create backend/data/input/items.json"
        )

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    movies = data.get("movies", [])
    gadgets = data.get("gadgets", [])
    vehicles = data.get("vehicles", [])

    results = {
        "movies": [],
        "gadgets": [],
        "vehicles": []
    }

    # Process movies
    if movies:
        print(f"\n=== Processing {len(movies)} movies ===")
        for movie_name in movies:
            try:
                result = _ingest_item(
                    category="movies",
                    item_name=movie_name,
                    release_date=None,
                    actor_names=None
                )
                results["movies"].append(result)
            except Exception as e:
                print(f"Error processing movie '{movie_name}': {e}")
                results["movies"].append({
                    "item_name": movie_name,
                    "success": False,
                    "error": str(e)
                })
    else:
        print("\n=== No movies to process ===")

    # Process gadgets
    if gadgets:
        print(f"\n=== Processing {len(gadgets)} gadgets ===")
        for gadget_name in gadgets:
            try:
                result = _ingest_item(
                    category="gadgets",
                    item_name=gadget_name,
                    release_date=None,
                    actor_names=None
                )
                results["gadgets"].append(result)
            except Exception as e:
                print(f"Error processing gadget '{gadget_name}': {e}")
                results["gadgets"].append({
                    "item_name": gadget_name,
                    "success": False,
                    "error": str(e)
                })
    else:
        print("\n=== No gadgets to process ===")

    # Process vehicles
    if vehicles:
        print(f"\n=== Processing {len(vehicles)} vehicles ===")
        for vehicle_name in vehicles:
            try:
                result = _ingest_item(
                    category="vehicles",
                    item_name=vehicle_name,
                    release_date=None,
                    actor_names=None
                )
                results["vehicles"].append(result)
            except Exception as e:
                print(f"Error processing vehicle '{vehicle_name}': {e}")
                results["vehicles"].append({
                    "item_name": vehicle_name,
                    "success": False,
                    "error": str(e)
                })
    else:
        print("\n=== No vehicles to process ===")

    return results


def _ingest_item(
    category: str,
    item_name: str,
    release_date: Optional[str] = None,
    actor_names: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Ingest a single item (movie, gadget, or vehicle)

    Args:
        category: "movies", "gadgets", or "vehicles"
        item_name: Name of the item
        release_date: Optional release date
        actor_names: Optional actor names (movies only, MAX 2)

    Returns:
        Dict with ingestion results
    """
    slug = _create_slug(item_name)

    # Initialize components for category
    if category == "movies":
        adapter = MoviesAdapter()
        store = JSONStore("movies", MOVIES_DIR)
        actor_names = actor_names[:2] if actor_names else []
    elif category == "gadgets":
        adapter = GadgetsAdapter()
        store = JSONStore("gadgets", GADGETS_DIR)
        actor_names = None
    else:
        adapter = VehiclesAdapter()
        store = JSONStore("vehicles", VEHICLES_DIR)
        actor_names = None

    curation_engine = CurationEngine(category)
    rag_synthesizer = RAGSynthesizer(category)

    # Load previous data if exists
    previous_data = store.load(slug)
    previous_summary = previous_data.get("summary") if previous_data else None

    # Step 1: Fetch comments
    print(f"\n[{category.upper()}] {item_name}")
    print(f"  → Fetching comments...")
    comments = adapter.fetch_comments(item_name)

    if not comments:
        raise ValueError(f"No comments found for '{item_name}'")

    print(f"  → Fetched {len(comments)} comments")

    # Step 2: Curate into buckets
    print(f"  → Curating buckets...")
    curation_result = curation_engine.curate(comments, actor_names)
    buckets = curation_result["buckets"]
    sentiment_counts = curation_result["sentiment_counts"]

    # Step 3: Synthesize summary (rolling RAG)
    print(f"  → Synthesizing summary...")
    summary = rag_synthesizer.synthesize(buckets, previous_summary)

    # Step 4: Fetch poster (movies only)
    poster_url = ""
    if category == "movies":
        print(f"  → Fetching poster from TMDB...")
        poster_url = _fetch_tmdb_poster(item_name)

    # Step 5: Save to storage
    data = {
        "title": item_name,
        "slug": slug,
        "category": category,
        "release_date": release_date,
        "last_updated_at": datetime.utcnow().isoformat(),
        "buckets": buckets,
        "sentiment_counts": sentiment_counts,
        "summary": summary,
        "poster_url": poster_url,
    }

    if actor_names:
        data["actor_names"] = actor_names

    store.save(slug, data)

    print(f"  ✓ Saved: {slug}")

    return {
        "success": True,
        "item_name": item_name,
        "slug": slug,
        "comments_processed": len(comments),
    }


def _fetch_tmdb_poster(movie_name: str) -> str:
    """Fetch movie poster URL from TMDB API"""
    if not TMDB_API_KEY:
        return ""
    try:
        query = urllib.parse.urlencode({"api_key": TMDB_API_KEY, "query": movie_name})
        url = f"{TMDB_BASE_URL}/search/movie?{query}"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read())
        results = data.get("results", [])
        if results and results[0].get("poster_path"):
            return f"{TMDB_IMAGE_BASE_URL}{results[0]['poster_path']}"
    except Exception as e:
        print(f"  TMDB poster fetch failed for '{movie_name}': {e}")
    return ""


def _create_slug(title: str) -> str:
    """Create URL-safe slug from title"""
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_-]+', '-', slug)
    slug = re.sub(r'^-+|-+$', '', slug)
    return slug
