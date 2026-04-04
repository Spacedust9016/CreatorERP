from core.module_base import ModuleBase
from core.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from fastapi import APIRouter
from typing import List
from pydantic import BaseModel


class NewsletterIssue(Base):
    __tablename__ = "newsletter_issues"
    id = Column(Integer, primary_key=True)
    issue_number = Column(Integer)
    title = Column(String(200))
    open_rate = Column(Float)
    click_rate = Column(Float)
    sent_at = Column(DateTime, default=datetime.utcnow)


class Subscriber(Base):
    __tablename__ = "subscribers"
    id = Column(Integer, primary_key=True)
    email = Column(String(200))
    source = Column(String(50))
    subscribed_at = Column(DateTime, default=datetime.utcnow)


class IssueMetrics(BaseModel):
    issue_number: int
    title: str
    open_rate: float
    click_rate: float
    sent_at: str


router = APIRouter(prefix="/api/newsletter", tags=["newsletter"])


@router.get("/metrics")
async def get_metrics():
    return {
        "subscribers": 8340,
        "open_rate": 58,
        "click_rate": 14,
        "churn_rate": 0.8,
        "growth_this_week": 142,
    }


@router.get("/issues", response_model=List[IssueMetrics])
async def get_issues():
    return [
        {
            "issue_number": 48,
            "title": "Productivity",
            "open_rate": 62,
            "click_rate": 18,
            "sent_at": "2026-04-03",
        },
        {
            "issue_number": 47,
            "title": "Tools roundup",
            "open_rate": 58,
            "click_rate": 14,
            "sent_at": "2026-03-27",
        },
        {
            "issue_number": 46,
            "title": "Tutorial deep-dive",
            "open_rate": 51,
            "click_rate": 11,
            "sent_at": "2026-03-20",
        },
        {
            "issue_number": 45,
            "title": "Case study",
            "open_rate": 64,
            "click_rate": 21,
            "sent_at": "2026-03-13",
        },
        {
            "issue_number": 44,
            "title": "Opinion piece",
            "open_rate": 48,
            "click_rate": 9,
            "sent_at": "2026-03-06",
        },
    ]


@router.get("/growth")
async def get_growth():
    return {
        "labels": ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr"],
        "data": [4200, 4900, 5500, 6100, 6900, 7800, 8340],
    }


@router.get("/sources")
async def get_sources():
    return {
        "labels": ["YouTube", "Instagram", "X", "Udemy", "Organic"],
        "data": [38, 28, 18, 11, 5],
    }


class NewsletterModule(ModuleBase):
    name = "newsletter"
    version = "1.0.0"
    description = "Newsletter analytics"
    models = [NewsletterIssue, Subscriber]

    def register_routes(self, app):
        app.include_router(router)

    def get_simulated_data(self):
        return {
            "metrics": {
                "subscribers": 8340,
                "open_rate": 58,
                "click_rate": 14,
                "churn_rate": 0.8,
            }
        }
