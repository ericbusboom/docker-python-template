"""Health-check endpoint — used by Docker and load balancers."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/api/health")
async def health():
    return JSONResponse({"status": "ok"})
