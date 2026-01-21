"""
PublicPulse Phase 0 - FastAPI Backend
Editorial intelligence platform for Movies and Gadgets
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.config import ALLOWED_ORIGINS
from app.api import movies_router, gadgets_router, vehicles_router
from app.core.ingestion import _ingest_item

# Initialize FastAPI
app = FastAPI(
    title="PublicPulse API",
    description="Editorial intelligence platform - Phase 0",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(movies_router)
app.include_router(gadgets_router)
app.include_router(vehicles_router)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


# Admin ingestion endpoint models
class IngestionRequest(BaseModel):
    category: str  # "movies", "gadgets", or "vehicles"
    item_name: str
    release_date: Optional[str] = None
    actor_names: Optional[List[str]] = None  # Movies only, MAX 2


@app.post("/admin/run-ingestion")
async def run_ingestion_endpoint(request: IngestionRequest):
    """
    Manual ingestion endpoint (protected in production)

    Workflow:
    1. Fetch YouTube comments via category adapter
    2. Curate into buckets using rule-based engine
    3. Synthesize summary using RAG (with rolling snapshot)
    4. Save to JSON storage
    """
    try:
        category = request.category.lower()

        if category not in ["movies", "gadgets", "vehicles"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid category. Must be 'movies', 'gadgets', or 'vehicles'"
            )

        # Use shared ingestion function
        result = _ingest_item(
            category=category,
            item_name=request.item_name,
            release_date=request.release_date,
            actor_names=request.actor_names
        )

        return {
            "success": result["success"],
            "slug": result["slug"],
            "message": f"Ingestion completed for '{request.item_name}'",
            "comments_processed": result["comments_processed"],
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        print(f"Ingestion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
