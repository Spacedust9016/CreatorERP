import click
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.main import cli, output_result, success, error, info


@cli.group()
@click.pass_context
def newsletter(ctx):
    """Manage newsletter analytics."""
    pass


@newsletter.command("metrics")
@click.pass_context
def newsletter_metrics(ctx):
    """Get newsletter metrics summary."""
    from modules.newsletter.module import NewsletterModule

    try:
        module = NewsletterModule()
        data = module.get_simulated_data()
        output_result(data["metrics"], ctx.obj["output"])
        success("Newsletter metrics retrieved")
    except Exception as e:
        error(f"Failed to get metrics: {e}")


@newsletter.command("issues")
@click.option("--limit", "-l", default=5, help="Number of issues to show")
@click.pass_context
def list_issues(ctx, limit):
    """List recent newsletter issues."""
    from modules.newsletter.module import NewsletterModule

    try:
        module = NewsletterModule()
        # Simulated issue data
        issues = [
            {
                "issue": 48,
                "title": "Productivity",
                "open_rate": 62,
                "click_rate": 18,
                "sent_at": "2026-04-03",
            },
            {
                "issue": 47,
                "title": "Tools roundup",
                "open_rate": 58,
                "click_rate": 14,
                "sent_at": "2026-03-27",
            },
            {
                "issue": 46,
                "title": "Tutorial deep-dive",
                "open_rate": 51,
                "click_rate": 11,
                "sent_at": "2026-03-20",
            },
            {
                "issue": 45,
                "title": "Case study",
                "open_rate": 64,
                "click_rate": 21,
                "sent_at": "2026-03-13",
            },
            {
                "issue": 44,
                "title": "Opinion piece",
                "open_rate": 48,
                "click_rate": 9,
                "sent_at": "2026-03-06",
            },
        ]
        output_result(issues[:limit], ctx.obj["output"])
        success(f"Retrieved {min(limit, len(issues))} issues")
    except Exception as e:
        error(f"Failed to list issues: {e}")


@newsletter.command("growth")
@click.pass_context
def subscriber_growth(ctx):
    """Get subscriber growth trend."""
    try:
        growth = {
            "labels": ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr"],
            "data": [4200, 4900, 5500, 6100, 6900, 7800, 8340],
            "total": 8340,
            "growth_rate": "+15.2%",
            "churn_rate": "0.8%",
        }
        output_result(growth, ctx.obj["output"])
        success("Growth data retrieved")
    except Exception as e:
        error(f"Failed to get growth: {e}")


@newsletter.command("sources")
@click.pass_context
def subscriber_sources(ctx):
    """Get subscriber acquisition sources."""
    try:
        sources = [
            {"source": "YouTube", "percentage": 38},
            {"source": "Instagram", "percentage": 28},
            {"source": "X", "percentage": 18},
            {"source": "Udemy", "percentage": 11},
            {"source": "Organic", "percentage": 5},
        ]
        output_result(sources, ctx.obj["output"])
        success("Source data retrieved")
    except Exception as e:
        error(f"Failed to get sources: {e}")
