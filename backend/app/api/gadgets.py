"""
Gadgets API endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict
from app.storage import JSONStore
from app.config import GADGETS_DIR

router = APIRouter(prefix="/gadgets", tags=["gadgets"])
store = JSONStore("gadgets", GADGETS_DIR)


@router.get("", response_model=List[Dict])
async def list_gadgets():
    """
    List all gadgets
    Returns: List of gadget objects with metadata and summaries
    """
    gadgets = store.list_all()
    return gadgets


@router.get("/{slug}", response_model=Dict)
async def get_gadget(slug: str):
    """
    Get a specific gadget by slug
    Returns: Gadget object with full details
    """
    gadget = store.load(slug)

    if not gadget:
        raise HTTPException(status_code=404, detail="Gadget not found")

    return gadget
