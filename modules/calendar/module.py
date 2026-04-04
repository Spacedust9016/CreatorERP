from core.module_base import ModuleBase
from core.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from fastapi import APIRouter
from typing import List, Optional
from pydantic import BaseModel


class ContentItem(Base):
    __tablename__ = "content_items"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    platform = Column(String(50))
    scheduled_date = Column(DateTime)
    status = Column(String(20))
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ContentSchedule(BaseModel):
    id: int
    title: str
    platform: str
    scheduled_date: str
    status: str
    notes: Optional[str] = None


class ContentCreate(BaseModel):
    title: str
    platform: str
    scheduled_date: str
    status: str = "Idea"
    notes: Optional[str] = None


router = APIRouter(prefix="/api/calendar", tags=["calendar"])


@router.get("/upcoming", response_model=List[ContentSchedule])
async def get_upcoming():
    return [
        {
            "id": 1,
            "title": "Video: 10 tools for creators",
            "platform": "YouTube",
            "scheduled_date": "2026-04-07",
            "status": "Draft",
        },
        {
            "id": 2,
            "title": "Newsletter #49",
            "platform": "Email",
            "scheduled_date": "2026-04-08",
            "status": "Ready",
        },
        {
            "id": 3,
            "title": "Thread: 1-year lessons",
            "platform": "X",
            "scheduled_date": "2026-04-09",
            "status": "Draft",
        },
        {
            "id": 4,
            "title": "Quick tip reel",
            "platform": "Instagram",
            "scheduled_date": "2026-04-10",
            "status": "Scheduled",
        },
        {
            "id": 5,
            "title": "Tutorial: beginner series ep.3",
            "platform": "YouTube",
            "scheduled_date": "2026-04-14",
            "status": "Idea",
        },
        {
            "id": 6,
            "title": "Newsletter #50 (milestone!)",
            "platform": "Email",
            "scheduled_date": "2026-04-15",
            "status": "Planning",
        },
    ]


@router.get("/month/{year}/{month}")
async def get_month(year: int, month: int):
    content_days = [3, 5, 7, 8, 10, 12, 14, 15, 17, 19, 21, 22, 24, 26, 28, 29]
    return {"year": year, "month": month, "content_days": content_days}


@router.post("/content")
async def create_content(content: ContentCreate):
    return {"message": "Content scheduled successfully", "content": content}


class CalendarModule(ModuleBase):
    name = "calendar"
    version = "1.0.0"
    description = "Content calendar management"
    models = [ContentItem]

    def register_routes(self, app):
        app.include_router(router)

    def get_simulated_data(self):
        return {
            "upcoming": [
                {
                    "date": "Apr 7",
                    "content": "Video: 10 tools for creators",
                    "platform": "YouTube",
                    "status": "Draft",
                },
                {
                    "date": "Apr 8",
                    "content": "Newsletter #49",
                    "platform": "Email",
                    "status": "Ready",
                },
                {
                    "date": "Apr 9",
                    "content": "Thread: 1-year lessons",
                    "platform": "X",
                    "status": "Draft",
                },
                {
                    "date": "Apr 10",
                    "content": "Quick tip reel",
                    "platform": "Instagram",
                    "status": "Scheduled",
                },
            ]
        }
