"""Data generation utilitiesfor simulated/demo data"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any


class DataSimulator:
    @staticmethod
    def generate_growth_data(
        months: int = 12, base: int = 1000, growth_rate: float = 0.15
    ) -> List[int]:
        data = [base]
        for i in range(1, months):
            noise = random.uniform(-0.05, 0.1)
            next_val = int(data[-1] * (1 + growth_rate / 12 + noise))
            data.append(max(next_val, data[-1]))
        return data

    @staticmethod
    def generate_revenue_sources(total: float) -> Dict[str, float]:
        udemy_pct = random.uniform(0.75, 0.85)
        adsense_pct = random.uniform(0.10, 0.15)
        sponsors_pct = 1 - udemy_pct - adsense_pct

        return {
            "udemy": round(total * udemy_pct, 2),
            "adsense": round(total * adsense_pct, 2),
            "sponsors": round(total * sponsors_pct, 2),
        }

    @staticmethod
    def generate_engagement_trend(weeks: int = 12) -> Dict[str, List[int]]:
        youtube_base = random.randint(100, 150)
        instagram_base = random.randint(70, 100)
        x_base = random.randint(30, 50)

        youtube_trend = DataSimulator.generate_growth_data(weeks, youtube_base, 0.25)
        instagram_trend = DataSimulator.generate_growth_data(
            weeks, instagram_base, 0.20
        )
        x_trend = DataSimulator.generate_growth_data(weeks, x_base, 0.18)

        return {
            "labels": [f"W{i}" for i in range(1, weeks + 1)],
            "youtube": youtube_trend,
            "instagram": instagram_trend,
            "x": x_trend,
        }

    @staticmethod
    def generate_post_performance(count: int = 10) -> List[Dict[str, Any]]:
        platforms = ["YouTube", "Instagram", "X"]
        content_types = {
            "YouTube": ["Tutorial:", "Video:", "Guide:"],
            "Instagram": ["Reel:", "Carousel:", "Story:"],
            "X": ["Thread:", "Hot take:", "Tips:"],
        }

        posts = []
        for i in range(count):
            platform = random.choice(platforms)
            content_prefix = random.choice(content_types[platform])
            reach = random.randint(5000, 50000)
            engagement = round(random.uniform(2.0, 8.0), 1)
            days_ago = random.randint(1, 14)

            posts.append(
                {
                    "platform": platform,
                    "content": f"{content_prefix} Creator tip #{i + 1}",
                    "reach": reach,
                    "engagement_rate": engagement,
                    "posted_at": (datetime.now() - timedelta(days=days_ago)).strftime(
                        "%Y-%m-%d"
                    ),
                }
            )

        return sorted(posts, key=lambda x: x["reach"], reverse=True)

    @staticmethod
    def generate_subscriber_sources() -> Dict[str, int]:
        return {"YouTube": 38, "Instagram": 28, "X": 18, "Udemy": 11, "Organic": 5}

    @staticmethod
    def generate_course_data() -> List[Dict[str, Any]]:
        courses = [
            {"title": "Complete guide to X", "hours": 8.5, "rating": 4.8},
            {"title": "Beginner's crash course", "hours": 3.2, "rating": 4.6},
            {"title": "Advanced masterclass", "hours": 12.0, "rating": 4.7},
            {"title": "Quick start series", "hours": 2.5, "rating": 4.5},
        ]

        for course in courses:
            course["students"] = random.randint(200, 1000)
            course["revenue"] = course["students"] * random.randint(8, 20)
            course["completion"] = round(random.uniform(60, 90), 0)

        return courses
