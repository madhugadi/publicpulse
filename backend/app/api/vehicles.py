"""
Vehicles API endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict
from app.storage import JSONStore
from app.config import VEHICLES_DIR

router = APIRouter(prefix="/vehicles", tags=["vehicles"])
store = JSONStore("vehicles", VEHICLES_DIR)


@router.get("", response_model=List[Dict])
async def list_vehicles():
    """
    List all vehicles
    Returns: List of vehicle objects with metadata and summaries
    """
    vehicles = store.list_all()
    return vehicles


@router.get("/{slug}", response_model=Dict)
async def get_vehicle(slug: str):
    """
    Get a specific vehicle by slug
    Returns: Vehicle object with full details
    """
    vehicle = store.load(slug)

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return vehicle
