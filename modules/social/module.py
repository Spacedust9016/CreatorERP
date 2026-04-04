from core.module_base import ModuleBase
from core.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import APIRouter, Depends
from core.database import get_db
from typing import List
from pydantic import BaseModel


class SocialPlatform(Base):
    __tablename__ = "social_platforms"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50))
    handle = Column(String(100))
    followers = Column(Integer, default=0)
    impressions_7d = Column(Integer, default=0)
    engagements = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    profile_visits = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)


class SocialPost(Base):
    __tablename__ = "social_posts"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50))
    content = Column(String(500))
    reach = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    posted_at = Column(DateTime, default=datetime.utcnow)


class PlatformMetrics(BaseModel):
    platform: str
    handle: str
    followers: int
    impressions_7d: int
    engagements: int
    engagement_rate: float
    profile_visits: int


class PostMetrics(BaseModel):
    platform: str
    content: str
    reach: int
    engagement_rate: float
    posted_at: datetime


router = APIRouter(prefix="/api/social", tags=["social"])


@router.get("/platforms", response_model=List[PlatformMetrics])
async def get_platforms(db: Session = Depends(get_db)):
    from .module import SocialModule

    module = SocialModule()
    return module.get_simulated_data()["platforms"]


@router.get("/posts", response_model=List[PostMetrics])
async def get_posts(db: Session = Depends(get_db)):
    from .module import SocialModule

    module = SocialModule()
    return module.get_simulated_data()["top_posts"]


@router.get("/engagement-trend")
async def get_engagement_trend():
    return {
        "labels": [
            "W1",
            "W2",
            "W3",
            "W4",
            "W5",
            "W6",
            "W7",
            "W8",
            "W9",
            "W10",
            "W11",
            "W12",
        ],
        "youtube": [120, 145, 160, 175, 200, 215, 210, 240, 258, 275, 295, 320],
        "instagram": [85, 95, 115, 132, 150, 158, 155, 172, 185, 198, 210, 222],
        "x": [40, 50, 55, 62, 70, 78, 75, 88, 90, 102, 112, 122],
    }


class SocialModule(ModuleBase):
    name = "social"
    version = "1.0.0"
    description = "Social media analytics and management"
    models = [SocialPlatform, SocialPost]

    def register_routes(self, app):
        app.include_router(router)

    def get_simulated_data(self):
        return {
            "platforms": [
                {
                    "platform": "X",
                    "handle": "@yourusername",
                    "followers": 18400,
                    "impressions_7d": 42000,
                    "engagements": 1240,
                    "engagement_rate": 2.9,
                    "profile_visits": 3100,
                },
                {
                    "platform": "Instagram",
                    "handle": "@yourusername",
                    "followers": 34200,
                    "impressions_7d": 67000,
                    "engagements": 4820,
                    "engagement_rate": 6.8,
                    "profile_visits": 2100,
                },
                {
                    "platform": "YouTube",
                    "handle": "Your Channel",
                    "followers": 71200,
                    "impressions_7d": 184000,
                    "engagements": 9200,
                    "engagement_rate": 4.7,
                    "profile_visits": 0,
                },
            ],
            "top_posts": [
                {
                    "platform": "X",
                    "content": "Thread: productivity hacks",
                    "reach": 24000,
                    "engagement_rate": 4.1,
                    "posted_at": "2026-04-01",
                },
                {
                    "platform": "Instagram",
                    "content": "Behind the scenes reel",
                    "reach": 18000,
                    "engagement_rate": 6.8,
                    "posted_at": "2026-04-02",
                },
                {
                    "platform": "YouTube",
                    "content": "Tutorial: build X in 10 min",
                    "reach": 52000,
                    "engagement_rate": 7.2,
                    "posted_at": "2026-03-28",
                },
                {
                    "platform": "Instagram",
                    "content": "Carousel: 5 tools I use",
                    "reach": 11000,
                    "engagement_rate": 3.4,
                    "posted_at": "2026-03-30",
                },
            ],
        }
