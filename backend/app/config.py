"""
Configuration for PublicPulse Phase 0
"""

from dotenv import load_dotenv
load_dotenv()
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MOVIES_DIR = DATA_DIR / "movies"
GADGETS_DIR = DATA_DIR / "gadgets"
VEHICLES_DIR = DATA_DIR / "vehicles"

# Ensure directories exist
MOVIES_DIR.mkdir(parents=True, exist_ok=True)
GADGETS_DIR.mkdir(parents=True, exist_ok=True)
VEHICLES_DIR.mkdir(parents=True, exist_ok=True)

# YouTube API
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")


# LLM API (Groq only - Phase 0 locked)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.1-8b-instant"  # Locked for Phase 0
GROQ_TEMPERATURE = 0.2  # Deterministic, editorial-safe output

# Ingestion limits
MAX_VIDEOS_PER_QUERY = 3
MAX_COMMENTS_PER_VIDEO = 50
MAX_TOTAL_COMMENTS_PER_ITEM = 200

# Curation limits (STRICT)
BUCKET_LIMITS = {
    "working": 3,
    "mixed": 2,
    "concerns": 2,
    "resonates": 2,
}

# YouTube query recency (days)
MOVIES_RECENCY_DAYS = 7
GADGETS_RECENCY_DAYS = 10
VEHICLES_RECENCY_DAYS = 10

# CORS
ALLOWED_ORIGINS = ["*"]

