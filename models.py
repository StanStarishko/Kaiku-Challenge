from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime


class AcceptanceStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Member(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    firstName: str
    lastName: str
    role: str
    pictureUrl: Optional[str] = None


class Raise(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    amountRaised: float


class Startup(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    name: str
    foundedYear: Optional[int] = None
    oneLiner: Optional[str] = None
    stage: Optional[str] = None
    industry: Optional[str] = None
    logoUrl: Optional[str] = None
    website: Optional[str] = None
    incorporatedLocation: Optional[str] = None
    fundraiseStage: Optional[str] = None
    targetRaise: Optional[float] = None
    targetEquity: Optional[float] = None
    productHighlights: Optional[List[str]] = []
    raises: Optional[List[Raise]] = []
    members: Optional[List[Member]] = []
    match: Optional[int] = None
    bookmarked: Optional[bool] = False
    status: AcceptanceStatus = AcceptanceStatus.PENDING
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: Optional[datetime] = None


class StartupCreate(BaseModel):
    name: str
    foundedYear: Optional[int] = None
    industry: Optional[str] = None
    stage: Optional[str] = None
    oneLiner: Optional[str] = None
    website: Optional[str] = None


class StartupUpdate(BaseModel):
    status: AcceptanceStatus