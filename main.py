import os
import uvicorn
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from uuid import UUID
from typing import Optional

from api import router as api_router
from api import update_startup_status, create_startup_api
from models import StartupCreate, StartupUpdate, AcceptanceStatus
from database import db

# Create FastAPI app
app = FastAPI(
    title="Startup Onboarding Platform",
    description="A simple backend for managing startup onboarding",
    version="1.0.0",
)

# Set up templates and static files
script_dir = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(script_dir, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(script_dir, "static")), name="static")

# Include API routes
app.include_router(api_router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main dashboard page"""
    startups = db.get_all_startups()
    
    # Count by status
    pending_count = len(db.get_pending_startups())
    accepted_count = len(db.get_accepted_startups())
    rejected_count = len(db.get_rejected_startups())
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "startups": startups,
            "pending_count": pending_count,
            "accepted_count": accepted_count,
            "rejected_count": rejected_count,
        }
    )


@app.get("/create", response_class=HTMLResponse)
async def create_form(request: Request):
    """Show the startup creation form"""
    return templates.TemplateResponse(
        "create.html",
        {"request": request}
    )


@app.post("/create")
async def create_startup(
    name: str = Form(...),
    founded_year: Optional[int] = Form(None),
    industry: Optional[str] = Form(None),
    stage: Optional[str] = Form(None),
    one_liner: Optional[str] = Form(None),
    website: Optional[str] = Form(None),
):
    """Handle startup creation form submission"""
    startup_data = StartupCreate(
        name=name,
        foundedYear=founded_year,
        industry=industry,
        stage=stage,
        oneLiner=one_liner,
        website=website
    )
    
    # Create startup via API
    startup = await create_startup_api(startup_data)
    
    # Redirect to dashboard
    return RedirectResponse(url="/", status_code=303)


@app.get("/view/{startup_id}", response_class=HTMLResponse)
async def view_startup(request: Request, startup_id: UUID):
    """View startup details"""
    startup = db.get_startup_by_id(startup_id)
    if startup is None:
        raise HTTPException(status_code=404, detail="Startup not found")
        
    return templates.TemplateResponse(
        "view.html",
        {"request": request, "startup": startup}
    )


@app.post("/update/{startup_id}")
async def update_startup(
    startup_id: UUID,
    status: str = Form(...),
):
    """Update startup status"""
    try:
        status_enum = AcceptanceStatus(status)
        update_data = StartupUpdate(status=status_enum)
        
        # Update via API
        await update_startup_status(startup_id, update_data)
        
        # Redirect to dashboard
        return RedirectResponse(url="/", status_code=303)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status value")


@app.get("/filter", response_class=HTMLResponse)
async def filter_startups(request: Request, status: str = "all"):
    """Filter startups by status"""
    if status == "accepted":
        startups = db.get_accepted_startups()
    elif status == "rejected":
        startups = db.get_rejected_startups()
    elif status == "pending":
        startups = db.get_pending_startups()
    else:
        startups = db.get_all_startups()
        
    # Count by status
    pending_count = len(db.get_pending_startups())
    accepted_count = len(db.get_accepted_startups())
    rejected_count = len(db.get_rejected_startups())
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "startups": startups,
            "pending_count": pending_count,
            "accepted_count": accepted_count,
            "rejected_count": rejected_count,
            "current_filter": status
        }
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5500, reload=True)