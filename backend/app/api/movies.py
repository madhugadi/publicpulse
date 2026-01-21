"""
Movies API endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict
from app.storage import JSONStore
from app.config import MOVIES_DIR

router = APIRouter(prefix="/movies", tags=["movies"])
store = JSONStore("movies", MOVIES_DIR)


@router.get("", response_model=List[Dict])
async def list_movies():
    """
    List all movies
    Returns: List of movie objects with metadata and summaries
    """
    movies = store.list_all()
    return movies


@router.get("/{slug}", response_model=Dict)
async def get_movie(slug: str):
    """
    Get a specific movie by slug
    Returns: Movie object with full details
    """
    movie = store.load(slug)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie
