from core.module_base import ModuleBase
from core.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from fastapi import APIRouter
from typing import List
from pydantic import BaseModel


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    platform = Column(String(50))
    duration_hours = Column(Float)
    students = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    revenue = Column(Float, default=0.0)
    status = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)


class CourseMetrics(BaseModel):
    title: str
    platform: str
    duration_hours: float
    students: int
    rating: float
    revenue: float
    status: str


router = APIRouter(prefix="/api/courses", tags=["courses"])


@router.get("/metrics")
async def get_metrics():
    return {
        "monthly_revenue": 3940,
        "total_students": 2190,
        "avg_rating": 4.7,
        "completion_rate": 68,
    }


@router.get("/list", response_model=List[CourseMetrics])
async def list_courses():
    from .module import CoursesModule

    module = CoursesModule()
    return module.get_simulated_data()["courses"]


@router.get("/revenue-trend")
async def get_revenue_trend():
    return {
        "labels": ["Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
        "data": [1800, 2100, 2400, 3100, 2800, 3200, 3600, 3940],
    }


class CoursesModule(ModuleBase):
    name = "courses"
    version = "1.0.0"
    description = "Course platform analytics"
    models = [Course]

    def register_routes(self, app):
        app.include_router(router)

    def get_simulated_data(self):
        return {
            "courses": [
                {
                    "title": "Complete guide to X",
                    "platform": "Udemy",
                    "duration_hours": 8.5,
                    "students": 840,
                    "rating": 4.8,
                    "revenue": 1680,
                    "status": "Bestseller",
                },
                {
                    "title": "Beginner's crash course",
                    "platform": "Udemy",
                    "duration_hours": 3.2,
                    "students": 920,
                    "rating": 4.6,
                    "revenue": 1470,
                    "status": "Hot",
                },
                {
                    "title": "Advanced masterclass",
                    "platform": "Udemy",
                    "duration_hours": 12.0,
                    "students": 430,
                    "rating": 4.7,
                    "revenue": 790,
                    "status": "Growing",
                },
            ]
        }
