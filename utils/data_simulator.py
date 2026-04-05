"""Data generation utilities for simulated/demo data."""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any


class DataSimulator:
    @staticmethod
    def _clamp(value: float, minimum: float, maximum: float) -> float:
        return max(minimum, min(maximum, value))

    @staticmethod
    def _format_compact(value: int) -> str:
        if value >= 1000000:
            return f"{value / 1000000:.1f}M"
        if value >= 1000:
            compact = value / 1000
            decimals = 0 if value >= 100000 else 1
            return f"{compact:.{decimals}f}K"
        return str(value)

    @staticmethod
    def _format_money(value: int) -> str:
        return f"${value:,}"

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

    @staticmethod
    def generate_live_snapshot() -> Dict[str, Any]:
        now = datetime.now()

        youtube_followers = random.randint(68000, 76000)
        instagram_followers = random.randint(30000, 38000)
        x_followers = random.randint(16000, 22000)

        total_reach = youtube_followers + instagram_followers + x_followers
        monthly_revenue = random.randint(4300, 6100)
        newsletter_subs = random.randint(7800, 9200)
        course_students = random.randint(2050, 2550)

        revenue_sources = DataSimulator.generate_revenue_sources(monthly_revenue)
        social_trend = DataSimulator.generate_engagement_trend()
        top_posts = DataSimulator.generate_post_performance(4)
        course_data = DataSimulator.generate_course_data()[:3]
        growth_points = DataSimulator.generate_growth_data(
            months=7, base=max(4200, newsletter_subs - 2600), growth_rate=0.20
        )

        issue_titles = [
            "Workflow teardown",
            "Creator systems",
            "Monetization notes",
            "Growth audit",
            "Behind the scenes",
        ]
        issues = []
        for index, title in enumerate(issue_titles, start=1):
            issue_number = 48 - (index - 1)
            issues.append(
                {
                    "issue_number": issue_number,
                    "title": title,
                    "open_rate": random.randint(46, 67),
                    "click_rate": random.randint(8, 23),
                    "sent_at": (now - timedelta(days=index * 7)).strftime("%Y-%m-%d"),
                }
            )

        content_days = sorted(random.sample(range(1, 31), 16))
        upcoming = []
        content_templates = [
            ("Video: Creator workflow breakdown", "YouTube"),
            ("Newsletter: Revenue notes", "Email"),
            ("Thread: Lessons from this week", "X"),
            ("Reel: One quick automation", "Instagram"),
            ("Tutorial: Beginner series", "YouTube"),
        ]
        statuses = ["Idea", "Draft", "Ready", "Scheduled", "Planning"]
        for offset, day in enumerate(content_days[:5], start=1):
            title, platform = content_templates[(offset - 1) % len(content_templates)]
            upcoming.append(
                {
                    "id": offset,
                    "title": title,
                    "platform": platform,
                    "scheduled_date": f"{now.year}-{now.month:02d}-{day:02d}",
                    "status": random.choice(statuses),
                }
            )

        activities = [
            {
                "event": "Short-form clip picked up momentum",
                "platform": "Instagram",
                "time": "12m ago",
                "impact": f"+{random.randint(180, 620)} plays",
                "positive": True,
            },
            {
                "event": "Course enrollment spike",
                "platform": "Udemy",
                "time": "34m ago",
                "impact": f"+${random.randint(45, 180)} revenue",
                "positive": True,
            },
            {
                "event": "Newsletter issue shipped",
                "platform": "Email",
                "time": "1h ago",
                "impact": f"{random.randint(48, 66)}% open rate",
                "positive": True,
            },
            {
                "event": "X thread slowed down",
                "platform": "X",
                "time": "2h ago",
                "impact": f"{random.randint(900, 2400)} impressions",
                "positive": False,
            },
            {
                "event": "New subscriber burst",
                "platform": "Website",
                "time": "3h ago",
                "impact": f"+{random.randint(15, 80)} signups",
                "positive": True,
            },
        ]

        platform_rows = [
            {
                "platform": "X",
                "handle": "@yourusername",
                "followers": x_followers,
                "impressions_7d": random.randint(32000, 61000),
                "engagements": random.randint(900, 1800),
                "engagement_rate": round(random.uniform(2.2, 4.8), 1),
                "profile_visits": random.randint(1800, 3900),
            },
            {
                "platform": "Instagram",
                "handle": "@yourusername",
                "followers": instagram_followers,
                "impressions_7d": random.randint(52000, 98000),
                "engagements": random.randint(3200, 6500),
                "engagement_rate": round(random.uniform(4.8, 8.1), 1),
                "profile_visits": random.randint(1500, 3400),
            },
            {
                "platform": "YouTube",
                "handle": "Your Channel",
                "followers": youtube_followers,
                "impressions_7d": random.randint(145000, 260000),
                "engagements": random.randint(7000, 14000),
                "engagement_rate": round(random.uniform(3.8, 6.4), 1),
                "profile_visits": random.randint(900, 2600),
            },
        ]

        course_revenue_trend = DataSimulator.generate_growth_data(
            months=8, base=1700, growth_rate=0.22
        )

        return {
            "generated_at": now.isoformat(),
            "overview": {
                "metrics": {
                    "total_reach": DataSimulator._format_compact(total_reach),
                    "monthly_revenue": DataSimulator._format_money(monthly_revenue),
                    "newsletter_subs": f"{newsletter_subs:,}",
                    "course_students": f"{course_students:,}",
                },
                "changes": {
                    "reach_change": f"{random.choice(['+', '-'])}{round(random.uniform(1.2, 6.4), 1)}% this week",
                    "revenue_change": f"{random.choice(['+', '-'])}{random.randint(2, 18)}% vs last month",
                    "subs_change": f"+{random.randint(40, 220)} this week",
                    "students_change": f"+{random.randint(12, 72)} this month",
                },
                "recent_activity": activities,
                "revenue_sources": revenue_sources,
                "audience": [youtube_followers, instagram_followers, x_followers],
            },
            "social": {
                "platforms": platform_rows,
                "top_posts": top_posts,
                "engagement_trend": social_trend,
            },
            "courses": {
                "metrics": {
                    "monthly_revenue": DataSimulator._format_money(monthly_revenue),
                    "total_students": f"{sum(course['students'] for course in course_data):,}",
                    "avg_rating": f"{round(sum(course['rating'] for course in course_data) / len(course_data), 1)}",
                    "completion_rate": f"{int(sum(course['completion'] for course in course_data) / len(course_data))}%",
                },
                "courses": course_data,
                "revenue_trend": {
                    "labels": ["Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
                    "data": course_revenue_trend,
                },
            },
            "newsletter": {
                "metrics": {
                    "subscribers": f"{newsletter_subs:,}",
                    "open_rate": f"{random.randint(50, 66)}%",
                    "click_rate": f"{random.randint(10, 21)}%",
                    "churn_rate": f"{round(DataSimulator._clamp(random.uniform(0.4, 1.4), 0.3, 1.5), 1)}%",
                },
                "issues": issues,
                "growth": {
                    "labels": ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr"],
                    "data": growth_points,
                },
                "sources": DataSimulator.generate_subscriber_sources(),
            },
            "calendar": {
                "month": {
                    "year": now.year,
                    "month": now.month,
                    "content_days": content_days,
                },
                "upcoming": upcoming,
            },
        }
