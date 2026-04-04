from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter(prefix="/api/overview", tags=["overview"])


@router.get("/")
async def get_overview() -> Dict[str, Any]:
    return {
        "metrics": {
            "total_reach": "124K",
            "monthly_revenue": "$4,820",
            "newsletter_subs": "8,340",
            "course_students": "2,190",
        },
        "changes": {
            "reach_change": "+3.2%",
            "revenue_change": "+12%",
            "subs_change": "+142 this week",
            "students_change": "+38 this month",
        },
        "recent_activity": [
            {
                "event": "New video published",
                "platform": "YouTube",
                "time": "2h ago",
                "impact": "+480 views",
            },
            {
                "event": "Newsletter #48 sent",
                "platform": "Email",
                "time": "Yesterday",
                "impact": "62% open rate",
            },
            {
                "event": "12 new enrollments",
                "platform": "Udemy",
                "time": "Yesterday",
                "impact": "+$180 revenue",
            },
            {
                "event": "Thread went viral",
                "platform": "X",
                "time": "2d ago",
                "impact": "+2.4K impressions",
            },
            {
                "event": "Reel published",
                "platform": "Instagram",
                "time": "3d ago",
                "impact": "820 plays",
            },
        ],
        "revenue_sources": {"udemy": 3940, "adsense": 620, "sponsors": 260},
    }


@router.get("/charts/revenue")
async def get_revenue_charts():
    return {
        "doughnut": {
            "data": [3940, 620, 260],
            "labels": ["Udemy", "AdSense", "Sponsors"],
            "colors": ["#378ADD", "#E24B4A", "#1D9E75"],
        }
    }


@router.get("/charts/audience")
async def get_audience_chart():
    return {
        "labels": ["YouTube", "Instagram", "X"],
        "data": [71200, 34200, 18400],
        "colors": ["#E24B4A", "#D85A30", "#378ADD"],
    }


def register_routes(app):
    app.include_router(router)
