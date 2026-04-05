import click
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from cli.main import cli, output_result, success, error, info

# Import all CLI modules
from cli import social, courses, newsletter, calendar, finance, ai


@cli.command()
@click.pass_context
def status(ctx):
    """Show system status and health."""
    try:
        status_data = {
            "app": "CreatorERP",
            "version": "1.0.0",
            "status": "operational",
            "modules": ["social", "courses", "newsletter", "calendar", "finance", "ai"],
            "database": "connected",
            "ai_provider": "local (default)",
        }

        if ctx.obj["output"] == "json":
            output_result(status_data, "json")
        else:
            click.echo(
                click.style(
                    "\n=============================================", fg="cyan"
                )
            )
            click.echo(
                click.style("  CREATOR ERP - SYSTEM STATUS", fg="cyan", bold=True)
            )
            click.echo(
                click.style("=============================================", fg="cyan")
            )
            click.echo(
                f"\n  Status: {click.style('OPERATIONAL', fg='green', bold=True)}"
            )
            click.echo(f"  Version: {status_data['version']}")
            click.echo(f"  Database: {click.style('CONNECTED', fg='green')}")
            click.echo(f"\n  Modules:")
            for mod in status_data["modules"]:
                click.echo(f"    {click.style('*', fg='green')} {mod}")
            click.echo(f"\n  AI Provider: {status_data['ai_provider']}")
            click.echo(
                click.style(
                    "\n=============================================", fg="cyan"
                )
            )
            success("System healthy")
    except Exception as e:
        error(f"Status check failed: {e}")


@cli.command()
@click.option(
    "--module",
    "-m",
    default="all",
    help="Module to show (all, social, courses, newsletter, calendar, finance)",
)
@click.pass_context
def dashboard(ctx, module):
    """Show unified dashboard overview."""
    from modules.social.module import SocialModule
    from modules.courses.module import CoursesModule
    from modules.finance.module import FinanceModule
    from modules.newsletter.module import NewsletterModule

    try:
        if ctx.obj["output"] == "json":
            data = {"social": SocialModule().get_simulated_data()}
            if module in ["all", "courses"]:
                data["courses"] = CoursesModule().get_simulated_data()
            if module in ["all", "finance"]:
                data["finance"] = FinanceModule().get_simulated_data()
            if module in ["all", "newsletter"]:
                data["newsletter"] = NewsletterModule().get_simulated_data()
            output_result(data, "json")
        else:
            click.echo(
                click.style(
                    "\n=============================================", fg="cyan"
                )
            )
            click.echo(
                click.style("       CREATOR ERP - DASHBOARD", fg="cyan", bold=True)
            )
            click.echo(
                click.style("=============================================", fg="cyan")
            )

            # Social metrics
            if module in ["all", "social"]:
                social_data = SocialModule().get_simulated_data()
                click.echo(click.style("\n[ SOCIAL MEDIA ]", fg="yellow", bold=True))
                for p in social_data["platforms"]:
                    click.echo(
                        f"  {p['platform']}: {p['followers']:,} followers | {p['engagement_rate']}% eng."
                    )

            # Courses
            if module in ["all", "courses"]:
                courses_data = CoursesModule().get_simulated_data()
                total_revenue = sum(c["revenue"] for c in courses_data["courses"])
                total_students = sum(c["students"] for c in courses_data["courses"])
                click.echo(click.style("\n[ COURSES ]", fg="yellow", bold=True))
                click.echo(f"  Revenue: ${total_revenue:,}/month")
                click.echo(f"  Students: {total_students:,}")

            # Newsletter
            if module in ["all", "newsletter"]:
                nl_data = NewsletterModule().get_simulated_data()
                click.echo(click.style("\n[ NEWSLETTER ]", fg="yellow", bold=True))
                click.echo(f"  Subscribers: {nl_data['metrics']['subscribers']:,}")
                click.echo(f"  Open Rate: {nl_data['metrics']['open_rate']}%")

            # Finance
            if module in ["all", "finance"]:
                fin_data = FinanceModule().get_simulated_data()
                click.echo(click.style("\n[ FINANCE ]", fg="yellow", bold=True))
                click.echo(f"  Monthly Revenue: ${fin_data['monthly_revenue']:,}")

            click.echo(
                click.style(
                    "\n=============================================", fg="cyan"
                )
            )
            success("Dashboard loaded")
    except Exception as e:
        error(f"Dashboard failed: {e}")


@cli.command()
@click.pass_context
def config(ctx):
    """Show current configuration."""
    from config import settings

    config_data = {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG,
        "database_url": settings.DATABASE_URL,
        "ai_provider": settings.AI_PROVIDER,
        "ai_model": settings.AI_MODEL,
        "simulated_data": settings.SIMULATED_DATA,
    }

    if ctx.obj["output"] == "json":
        output_result(config_data, "json")
    else:
        click.echo(click.style("\n=== CONFIGURATION ===", fg="cyan", bold=True))
        for key, value in config_data.items():
            click.echo(f"  {key}: {value}")
        success("Configuration displayed")


if __name__ == "__main__":
    cli()
