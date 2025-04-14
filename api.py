from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from models import Startup, StartupCreate, StartupUpdate, AcceptanceStatus
from database import db

router = APIRouter()


@router.get("/startups", response_model=List[Startup], tags=["startups"])
async def get_startups(
    status: Optional[str] = Query(None, description="Filter by status: pending, accepted, rejected")
):
    """
    Get all startups, optionally filtered by status
    """
    if status == "accepted":
        return db.get_accepted_startups()
    elif status == "rejected":
        return db.get_rejected_startups()
    elif status == "pending":
        return db.get_pending_startups()
    else:
        return db.get_all_startups()


@router.get("/startups/{startup_id}", response_model=Startup, tags=["startups"])
async def get_startup(startup_id: UUID):
    """
    Get a specific startup by ID
    """
    startup = db.get_startup_by_id(startup_id)
    if startup is None:
        raise HTTPException(status_code=404, detail="Startup not found")
    return startup


@router.post("/startups", response_model=Startup, tags=["startups"])
async def create_startup_api(startup_data: StartupCreate):
    """
    Create a new startup
    """
    # Convert StartupCreate to full Startup
    startup = Startup(
        name=startup_data.name,
        foundedYear=startup_data.foundedYear,
        industry=startup_data.industry,
        stage=startup_data.stage,
        oneLiner=startup_data.oneLiner,
        website=startup_data.website,
        status=AcceptanceStatus.PENDING
    )
    return db.create_startup(startup)


@router.put("/startups/{startup_id}", response_model=Startup, tags=["startups"])
async def update_startup_status(startup_id: UUID, update_data: StartupUpdate):
    """
    Update a startup's acceptance status
    """
    updated_startup = db.update_startup(startup_id, update_data.status)
    if updated_startup is None:
        raise HTTPException(status_code=404, detail="Startup not found")
    return updated_startup