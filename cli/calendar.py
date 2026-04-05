import click
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.main import cli, output_result, success, error, info


@cli.group()
@click.pass_context
def calendar(ctx):
    """Manage content calendar."""
    pass


@calendar.command("upcoming")
@click.option("--days", "-d", default=14, help="Number of days ahead")
@click.pass_context
def upcoming_content(ctx, days):
    """Show upcoming scheduled content."""
    from modules.calendar.module import CalendarModule

    try:
        module = CalendarModule()
        data = module.get_simulated_data()

        upcoming = data["upcoming"]
        output_result(upcoming, ctx.obj["output"])
        success(f"Found {len(upcoming)} upcoming items")
    except Exception as e:
        error(f"Failed to get upcoming: {e}")


@calendar.command("add")
@click.option("--title", "-t", required=True, help="Content title")
@click.option(
    "--platform",
    "-p",
    required=True,
    type=click.Choice(["YouTube", "Instagram", "X", "Email", "TikTok"]),
    help="Platform",
)
@click.option("--date", "-d", required=True, help="Scheduled date (YYYY-MM-DD)")
@click.option(
    "--status",
    "-s",
    default="Idea",
    type=click.Choice(["Idea", "Draft", "Ready", "Scheduled", "Published"]),
    help="Content status",
)
@click.pass_context
def add_content(ctx, title, platform, date, status):
    """Add new content to calendar."""
    try:
        content = {
            "title": title,
            "platform": platform,
            "scheduled_date": date,
            "status": status,
            "created_at": datetime.now().isoformat(),
        }
        output_result(content, ctx.obj["output"])
        success(f"Content '{title}' added for {date}")
        info("Note: This is simulated. Connect to database for persistence.")
    except Exception as e:
        error(f"Failed to add content: {e}")


@calendar.command("week")
@click.pass_context
def calendar_week(ctx):
    """Show content for the current week."""
    try:
        today = datetime.now()
        start = today - timedelta(days=today.weekday())

        week_content = []
        for item in [
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
        ]:
            week_content.append(item)

        if ctx.obj["output"] == "json":
            output_result(week_content, "json")
        else:
            click.echo(
                click.style("\n=== THIS WEEK'S CONTENT ===", fg="cyan", bold=True)
            )
            for item in week_content:
                status_color = (
                    "green" if item["status"] in ["Ready", "Scheduled"] else "yellow"
                )
                click.echo(f"{item['date']}: [{item['platform']}] {item['content']}")
            success("Week calendar displayed")
    except Exception as e:
        error(f"Failed to show week: {e}")


@calendar.command("status")
@click.argument("content_id", type=int)
@click.argument(
    "new_status",
    type=click.Choice(["Idea", "Draft", "Ready", "Scheduled", "Published"]),
)
@click.pass_context
def update_status(ctx, content_id, new_status):
    """Update content status."""
    try:
        click.echo(f"Content {content_id} status updated to: {new_status}")
        success("Status updated (simulated)")
    except Exception as e:
        error(f"Failed to update: {e}")
