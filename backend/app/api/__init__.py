from .movies import router as movies_router
from .gadgets import router as gadgets_router
from .vehicles import router as vehicles_router

__all__ = ["movies_router", "gadgets_router", "vehicles_router"]
